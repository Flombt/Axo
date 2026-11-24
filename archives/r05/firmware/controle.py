"""Etat local et commandes du prototype AURA-01 r05."""
from math import copysign, isfinite, sqrt

AXES = ("J1", "J2", "J3", "P", "I", "MAU")
# Le poignet est manuel. Les consignes sont des angles de sortie, en degrés.
BOUNDS = ((-88, 88), (-18, 18), (-22, 22), (0, 92), (0, 92), (0, 92))
RATES = (22, 14, 18, 42, 42, 42)
ACCELERATIONS = (50, 35, 50, 150, 150, 150)
DRIVE_RATIO = (-22 / 38, -3, -2, 1, 1, 1)
PERIOD_MS = 20
DEADMAN_MS = 350


def parse(line):
    parts = line.split()
    if not parts:
        raise ValueError("commande vide")
    op = parts[0].upper()
    if len(parts) == 1 and op in ("PING", "STATUS", "STOP", "ARM"):
        return op, {}
    if op != "MOVE" or len(parts) < 2:
        raise ValueError("commande inconnue")
    q = {}
    for token in parts[1:]:
        axis, equal, raw = token.partition("=")
        axis = axis.upper()
        if equal != "=" or axis not in AXES or axis in q:
            raise ValueError("axe inconnu ou répété")
        i = AXES.index(axis)
        v = float(raw)
        lo, hi = BOUNDS[i]
        if not isfinite(v) or not lo <= v <= hi:
            raise ValueError("hors course")
        q[axis] = v
    return op, q


class Motion:
    def __init__(self, commissioned=False):
        self.commissioned = commissioned
        self.armed = False
        self.reason = "boot"
        self.last_command = 0
        self.position = [0.0] * len(AXES)
        self.goal = self.position[:]
        self.velocity = [0.0] * len(AXES)

    def stop(self, reason):
        self.armed = False
        self.reason = reason

    def command(self, line, now):
        op, values = parse(line)
        if op in ("PING", "MOVE") and self.armed:
            self.last_command = now
        if op == "STOP":
            self.stop("stop")
        elif op == "ARM":
            if self.armed:
                raise ValueError("déjà armé")
            if not self.commissioned:
                raise ValueError("étalonnage requis")
            self.last_command = now
            self.position = [0.0] * len(AXES)
            self.goal = self.position[:]
            self.velocity = [0.0] * len(AXES)
            self.reason = "armé"
            self.armed = True
        elif op == "MOVE":
            if not self.armed:
                raise ValueError("sorties coupées")
            for key, value in values.items():
                self.goal[AXES.index(key)] = value
        return op

    def tick(self, now, ticks_diff):
        if not self.armed:
            return None
        if ticks_diff(now, self.last_command) >= DEADMAN_MS:
            self.stop("timeout")
            return None
        elapsed = PERIOD_MS / 1000
        for i, speed in enumerate(RATES):
            delta = self.goal[i] - self.position[i]
            acceleration = ACCELERATIONS[i]
            wish = copysign(min(speed, sqrt(2 * acceleration * abs(delta))), delta)
            change = max(-acceleration * elapsed,
                         min(acceleration * elapsed, wish - self.velocity[i]))
            self.velocity[i] += change
            step = self.velocity[i] * elapsed
            if step * delta >= 0 and abs(step) >= abs(delta):
                self.position[i] = self.goal[i]
                self.velocity[i] = 0.0
            else:
                lo, hi = BOUNDS[i]
                candidate = self.position[i] + step
                self.position[i] = max(lo, min(hi, candidate))
                if candidate != self.position[i]:
                    self.velocity[i] = 0.0
        return self.position


def pulse_us(command, i, profile):
    zero, micros_per_degree, lower, upper = profile[i]
    value = round(zero + command * DRIVE_RATIO[i] * micros_per_degree)
    if not (lower <= value <= upper):
        raise ValueError("impulsion hors étalonnage")
    return value
