"""Essais hôte du contrôleur et des défauts bloquants de la V5."""
import unittest

from controle import Calibration, Supervisor
from enveloppe import LIMITS, REVISION


def data():
    # Valeurs synthétiques pour exercer le parseur et les limites. Aucun PWM de montage.
    return {"revision":REVISION, "rail_adc_v_max":6.6,
            "pwm_us":{k:[[lo, 1000], [hi, 2000]] for k,(lo,hi) in LIMITS.items()},
            "pitch_adc_u16":{"J2":[[-24, 9000], [24, 55000]],"J3":[[-35, 55000],[35, 8000]]}}


class ControlTest(unittest.TestCase):
    def setUp(self):
        self.profile = Calibration(data())
        self.s = Supervisor(self.profile, lambda new, old: new-old)
        self.now = 0

    def step(self, dt=10, rail=5.15, current=0, arm=False, stop=True, sensor=True, pitch=None):
        self.now += dt
        if pitch is None:
            pitch = {k:self.s.sent[k] for k in ("J2","J3")}
        self.s.tick(self.now, stop, arm, rail, current, sensor, pitch)

    def command(self, text):
        return self.s.command(text, self.now)

    def power(self, held=False):
        self.step(rail=0.0)
        self.step(arm=held)
        self.step(250, arm=held)

    def arm(self):
        self.power()
        self.command("PING")
        self.step(arm=True)
        self.assertEqual(self.s.state,"ARMED")
        self.assertTrue(self.s.pwm)

    def test_missing_calibration_cannot_enable_relay_or_pwm(self):
        self.s.cal = None
        self.power()
        self.command("PING")
        self.step(arm=True)
        self.assertFalse(self.s.relay or self.s.pwm)
        self.assertEqual(self.command("MOVE J1 1"),"ERR DESARME")

    def test_invalid_and_monotonic_calibration(self):
        for path, value in (("revision","r05"), ("rail_adc_v_max", float("nan")),
                            ("pwm_us",{}), ("pitch_adc_u16",{})):
            candidate = data()
            candidate[path] = value
            with self.subTest(field=path), self.assertRaises(ValueError):
                Calibration(candidate)
        candidate = data()
        candidate["pwm_us"]["J1"] = [[-88, 1000],[0, 1750],[88, 1700]]
        with self.assertRaises(ValueError):
            Calibration(candidate)
        self.assertAlmostEqual(self.profile.pitch("J2",32000),0)
        self.assertAlmostEqual(self.profile.pitch("J3",31500),0)
        self.assertEqual(self.profile.pulse("J1",0),1500)

    def test_no_autostart_held_button_usb_reset(self):
        self.power(held=True)
        for _ in range(20):
            self.command("PING")
            self.step(30,arm=True)
        self.assertEqual(self.s.state,"READY")
        self.s = Supervisor(self.profile, lambda a,b: a-b)
        self.power(held=True)
        self.command("PING")
        self.step(arm=True)
        self.assertFalse(self.s.pwm)
        self.step()
        self.step(arm=True)
        self.assertTrue(self.s.pwm)

    def test_manual_arm_requires_park_and_heartbeat(self):
        self.power()
        self.step(arm=True)
        self.assertEqual(self.s.fault,"absence_ping_avant_armement")
        self.step(rail=0)
        self.assertEqual(self.command("RESET"),"OK RESET")
        self.power()
        self.command("PING")
        self.step(arm=True,pitch={"J2": 4, "J3": 0})
        self.assertEqual(self.s.fault,"position_de_parc")

    def test_parser_atomic_bounds_all_nine(self):
        self.arm()
        clipped = self.s.target.copy()
        for line in ("MOVE", "MOVE J1", "MOVE J1 nan", "MOVE J1 inf", "MOVE J1 -1e100",
                     "MOVE J1 5 J1 6", "MOVE J1 1 J2R 2", "MOVE J1 89", "MOVE J2 -21 J3 -32",
                     "MOVE Servo_P -1", "MOVE Servo_U 93", "MOVE J7 31", "PING foo"):
            with self.subTest(command=line):
                self.assertTrue(self.command(line).startswith("ERR"))
                self.assertEqual(clipped,self.s.target)
        for key in LIMITS:
            self.assertEqual(self.command("MOVE " + key + " 5"),"OK")
        for i in range(50):
            if i % 10 == 0:
                self.command("PING")
            prior = self.s.sent.copy()
            self.step(20)
            for k in prior:
                self.assertGreaterEqual(self.s.sent[k],prior[k])
        self.assertEqual(set(self.s.sent.values()),{5.0})

    def test_cross_corner_and_legitimate_escape(self):
        self.arm()
        self.s.sent.update(J2=-21,J3=-19)
        self.s.target = self.s.sent.copy()
        self.s.measured = {"J2": -21, "J3": -19}
        self.assertEqual(self.command("MOVE J2 15 J3 -32"),"ERR ENVELOPPE")
        self.assertEqual(self.command("MOVE J2 15"),"OK")
        self.s.sent.update(J2=-21,J3=-65/3)
        self.s.target = self.s.sent.copy()
        self.s.measured = {"J2": -21, "J3": -65/3}
        self.assertEqual(self.command("MOVE J3 0"),"OK")

    def test_rail_drop_and_return_latch(self):
        self.arm()
        self.assertEqual(self.command("MOVE J1 10"),"OK")
        self.step(rail=4.72)
        self.assertEqual(self.s.fault,"perte_rail")
        self.step(rail=5.15,arm=True)
        self.assertFalse(self.s.pwm or self.s.relay)
        self.assertEqual(self.command("RESET"),"ERR RESET")
        self.step(rail=.14)
        self.assertEqual(self.command("RESET"),"OK RESET")
        self.power(held=True)
        self.assertFalse(self.s.pwm)

    def test_disconnect_stop_and_bad_sensor(self):
        for argument, expected in (({"dt":351}, "communication"), ({"stop":False},"stop_materiel"),
                                   ({"sensor":False},"mesure_indisponible"),({"rail":5.4},"surtension"),
                                   ({"pitch":{"J2":-23,"J3":-31}},"pose_mesuree")):
            with self.subTest(cause=expected):
                self.setUp()
                self.arm()
                self.step(**argument)
                self.assertEqual(self.s.fault,expected)
                self.assertFalse(self.s.pwm or self.s.relay)
        self.setUp()
        self.arm()
        self.assertEqual(self.command("STOP"),"OK STOP")
        self.assertFalse(self.s.pwm or self.s.relay)

    def test_stall_and_tracking_faults(self):
        self.arm()
        self.step(current=12.7)
        self.step(90,current=12.7)
        self.assertEqual(self.s.state,"ARMED")
        self.step(10,current=12.7)
        self.assertEqual(self.s.fault,"surintensite")
        self.setUp()
        self.arm()
        self.step(pitch={"J2":9,"J3":0})
        self.step(180,pitch={"J2":9,"J3":0})
        self.assertEqual(self.s.fault,"suivi_tangage")


if __name__ == "__main__":
    unittest.main(verbosity=2)
