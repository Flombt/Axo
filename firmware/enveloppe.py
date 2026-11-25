"""Limites de consigne de la V5 stabilisée, en degrés."""
REVISION = "V5-stabilisation"
PINS = {"J1": 2, "J2": 3, "J3": 4, "J7": 5,
        "Servo_P": 6, "Servo_I": 7, "Servo_M": 8, "Servo_A": 9, "Servo_U": 10}
LIMITS = {"J1": (-88, 88), "J2": (-21, 21), "J3": (-32, 32), "J7": (-30, 30),
          "Servo_P": (0, 92), "Servo_I": (0, 92), "Servo_M": (0, 92),
          "Servo_A": (0, 92), "Servo_U": (0, 92)}
RATES = {"J1": 20, "J2": 12, "J3": 14, "J7": 16,
         "Servo_P": 30, "Servo_I": 30, "Servo_M": 30, "Servo_A": 30, "Servo_U": 30}
GP_ARM = 12
GP_STOP_OK = 13
GP_POWER_PERMIT = 14
GP_PWM_ENABLE = 15
GP_J2_FEEDBACK = 26
GP_J3_FEEDBACK = 27
GP_RAIL = 28

# Le point le plus bas du rectangle de transition borne le cas où un servo prend du retard.
def coupled(j2, j3, limit=-34.0):
    return j2 + 0.6 * j3 >= limit - 1e-9


def pose_ok(pose):
    return (all(low <= pose[key] <= high for key, (low, high) in LIMITS.items())
            and coupled(pose["J2"], pose["J3"]))


def transition_ok(start, end):
    return coupled(min(start["J2"], end["J2"]), min(start["J3"], end["J3"]), -36.0)
