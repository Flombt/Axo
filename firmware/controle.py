"""Superviseur de banc, déterministe et indépendant des entrées/sorties."""
import math
from enveloppe import LIMITS, RATES, REVISION, coupled, pose_ok, transition_ok

HEARTBEAT_MS = 350
RAIL_STABLE_MS = 250
TRACKING_DELAY_MS = 180
OVERCURRENT_MS = 100
SAFE_RAIL_V = (5.00, 5.35)
CURRENT_TRIP_A = 12.5
MAX_TRACKING_ERROR_DEG = 4
PITCH_AXES = ("J2", "J3")


def finite(number):
    if not isinstance(number, (float, int)) or isinstance(number, bool):
        return False
    return math.isfinite(number)


def verify_table(points, minimum, maximum):
    if not isinstance(points, list) or len(points) < 2:
        raise ValueError("points_calibration")
    if any(not isinstance(row, list) or len(row) != 2 for row in points):
        raise ValueError("ligne_calibration")
    xx = [row[0] for row in points]
    yy = [row[1] for row in points]
    if (not all(finite(v) for v in xx + yy) or xx[0] > minimum or xx[-1] < maximum
            or not all(a < b for a, b in zip(xx, xx[1:]))
            or not (all(a < b for a, b in zip(yy, yy[1:])) or all(a > b for a, b in zip(yy, yy[1:])))):
        raise ValueError("courbe_calibration")
    return xx, yy


def interpolate(points, x):
    for (a, va), (b, vb) in zip(points, points[1:]):
        if a <= x <= b:
            return va + (vb - va) * (x - a) / (b - a)
    raise ValueError("hors_calibration")


class Calibration:
    def __init__(self, data):
        if data.get("revision") != REVISION:
            raise ValueError("revision_calibration")
        self.outputs = data["pwm_us"]
        self.inputs = data["pitch_adc_u16"]
        if set(self.outputs) != set(LIMITS) or set(self.inputs) != set(PITCH_AXES):
            raise ValueError("axes_calibration")
        for key, (low, high) in LIMITS.items():
            xx, yy = verify_table(self.outputs[key], low, high)
            if not all(700 <= y <= 2300 for y in yy):
                raise ValueError("largeur_impulsion")
        for key in PITCH_AXES:
            low, high = LIMITS[key]
            xx, yy = verify_table(self.inputs[key], low - 2, high + 2)
            if not all(800 <= y <= 64700 for y in yy) or abs(yy[0] - yy[-1]) < 4000:
                raise ValueError("plage_capteur")
            # Transformer la courbe angle -> ADC en courbe ADC -> angle.
            self.inputs[key] = sorted([[y, x] for x, y in self.inputs[key]])
        self.rail_factor = data["rail_adc_v_max"]
        if not finite(self.rail_factor) or not 6.3 <= self.rail_factor <= 6.9:
            raise ValueError("echelle_rail")

    def pulse(self, key, angle):
        return round(interpolate(self.outputs[key], angle))

    def pitch(self, key, raw):
        return interpolate(self.inputs[key], raw)


class Supervisor:
    def __init__(self, calibration, ticks_diff):
        self.cal = calibration
        self.diff = ticks_diff
        self.state = "OFF"
        self.fault = ""
        self.stop_ok = False
        self.arm_released = False
        self.relay = False
        self.pwm = False
        self.power_since = None
        self.last_ping = None
        self.last_tick = None
        self.tracking_since = None
        self.over_since = None
        self.measured = {}
        self.sent = dict.fromkeys(LIMITS, 0.0)
        self.target = self.sent.copy()
        self.rail_v = 0.0
        self.current_a = 0.0

    def trip(self, reason):
        self.state = "FAULT"
        self.fault = reason
        self.relay = self.pwm = False
        self.power_since = self.last_ping = self.tracking_since = self.over_since = None
        self.arm_released = False
        self.target = self.sent.copy()

    def tick(self, now, stop_ok, arm_down, volts, amps, sensor_ok, angles):
        self.stop_ok = stop_ok
        self.rail_v, self.current_a, self.measured = volts, amps, angles
        elapsed = 0 if self.last_tick is None else max(0, self.diff(now, self.last_tick))
        self.last_tick = now
        if not stop_ok:
            if self.state != "FAULT":
                self.trip("stop_materiel")
            return
        if self.state == "FAULT":
            return
        if self.cal is None:
            return
        if not sensor_ok or not finite(volts) or not finite(amps) or amps < -.25:
            self.trip("mesure_indisponible")
            return
        self.relay = True
        rail_good = SAFE_RAIL_V[0] <= volts <= SAFE_RAIL_V[1]
        if volts > SAFE_RAIL_V[1]:
            self.trip("surtension")
            return
        if not rail_good:
            if self.state in ("READY", "ARMED"):
                self.trip("perte_rail")
            else:
                self.power_since = None
            return
        if self.power_since is None:
            self.power_since = now
        if amps > CURRENT_TRIP_A:
            if self.over_since is None:
                self.over_since = now
            if self.diff(now, self.over_since) >= OVERCURRENT_MS:
                self.trip("surintensite")
                return
        else:
            self.over_since = None

        if self.state == "OFF" and self.diff(now, self.power_since) >= RAIL_STABLE_MS:
            self.state = "READY"
            self.arm_released = False
        if self.state == "READY":
            if not arm_down:
                self.arm_released = True
            elif self.arm_released:
                self.arm_released = False
                self.arm(now)
        if self.state != "ARMED":
            return
        if elapsed > HEARTBEAT_MS or self.diff(now, self.last_ping) > HEARTBEAT_MS:
            self.trip("communication")
            return
        if (not all(finite(angles.get(k)) for k in PITCH_AXES)
                or not coupled(angles["J2"] - 1, angles["J3"] - 1, -36.0)
                or any(not LIMITS[k][0] - 2 <= angles[k] <= LIMITS[k][1] + 2 for k in PITCH_AXES)):
            self.trip("pose_mesuree")
            return
        if any(abs(angles[k] - self.sent[k]) > MAX_TRACKING_ERROR_DEG for k in PITCH_AXES):
            if self.tracking_since is None:
                self.tracking_since = now
            if self.diff(now, self.tracking_since) >= TRACKING_DELAY_MS:
                self.trip("suivi_tangage")
                return
        else:
            self.tracking_since = None
        self.advance(min(elapsed, 40) / 1000.0)

    def arm(self, now):
        if not all(finite(self.measured.get(k)) and abs(self.measured[k]) <= 2 for k in PITCH_AXES):
            self.trip("position_de_parc")
            return
        if self.last_ping is None or self.diff(now, self.last_ping) > HEARTBEAT_MS:
            self.trip("absence_ping_avant_armement")
            return
        self.sent = dict.fromkeys(LIMITS, 0.0)
        self.target = self.sent.copy()
        self.pwm = True
        self.state = "ARMED"

    def advance(self, dt):
        duration = max(abs(self.target[k] - angle) / RATES[k] for k, angle in self.sent.items())
        if duration == 0:
            return
        part = min(1, dt / duration)
        next_pose = {k: angle + part * (self.target[k] - angle) for k, angle in self.sent.items()}
        if not pose_ok(next_pose):
            self.trip("enveloppe")
        else:
            self.sent = next_pose

    def move(self, words):
        if self.state != "ARMED":
            return "ERR DESARME"
        if not words or len(words) % 2 or len(words) > len(LIMITS) * 2:
            return "ERR PAIRES"
        proposal = self.target.copy()
        seen = set()
        for index in range(0, len(words), 2):
            key, raw = words[index:index+2]
            if key not in LIMITS or key in seen:
                return "ERR AXE"
            try:
                value = float(raw)
            except ValueError:
                return "ERR NOMBRE"
            if not finite(value):
                return "ERR NOMBRE"
            seen.add(key)
            proposal[key] = value
        # Prévoir aussi le cas où le servo suit la dernière pose mesurée avec retard.
        worst = {k: min(self.sent[k], self.measured[k] - 1) for k in PITCH_AXES}
        if not pose_ok(proposal) or not transition_ok(worst, proposal):
            return "ERR ENVELOPPE"
        self.target = proposal
        return "OK"

    def command(self, line, now):
        words = line.split()
        if not words:
            return "ERR COMMANDE"
        cmd = words[0]
        if cmd == "MOVE":
            return self.move(words[1:])
        if len(words) != 1:
            return "ERR SYNTAXE"
        if cmd == "PING":
            self.last_ping = now
            return "PONG"
        if cmd == "STOP":
            self.trip("stop_serie")
            return "OK STOP"
        if cmd == "RESET":
            if self.state != "FAULT" or not self.stop_ok or not finite(self.rail_v) or abs(self.rail_v) >= .4:
                return "ERR RESET"
            self.state = "OFF"
            self.fault = ""
            self.last_ping = None
            return "OK RESET"
        if cmd == "STATUS":
            return {"state": self.state, "fault": self.fault, "relay": self.relay, "pwm": self.pwm,
                    "volt": self.rail_v, "amp": self.current_a, "target": self.target,
                    "sent": self.sent, "pitch_deg": self.measured, "calibrated": self.cal is not None}
        return "ERR COMMANDE"
