"""Point d'entrée MicroPython pour Pico 2 RP2350 et faisceau V5 stabilisé."""
import json
import sys
import time

import machine
import select

from controle import Calibration, Supervisor
from enveloppe import (GP_ARM, GP_J2_FEEDBACK, GP_J3_FEEDBACK, GP_POWER_PERMIT,
                        GP_PWM_ENABLE, GP_RAIL, GP_STOP_OK, PINS)

BAUD_PWM = 50
SHUNT_OHM = .002
SENSOR_ADDR = 0x40
LINE_LIMIT = 296


class Board:
    def __init__(self):
        self.power = machine.Pin(GP_POWER_PERMIT, machine.Pin.OUT, value=0)
        self.enable = machine.Pin(GP_PWM_ENABLE, machine.Pin.OUT, value=0)
        self.stop_ok = machine.Pin(GP_STOP_OK, machine.Pin.IN)
        self.arm = machine.Pin(GP_ARM, machine.Pin.IN)
        self.rail = machine.ADC(GP_RAIL)
        self.pitch_sensors = {"J2": machine.ADC(GP_J2_FEEDBACK), "J3": machine.ADC(GP_J3_FEEDBACK)}
        self.bus = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=100000, timeout=15000)
        self.sensor_ready = False
        self.outputs = {}
        self.last = {}

    def sample(self, profile):
        volts = self.rail.read_u16() * (profile.rail_factor if profile else 6.6) / 65535
        try:
            if not self.sensor_ready:
                maker = self.bus.readfrom_mem(SENSOR_ADDR, 254, 2)
                die = self.bus.readfrom_mem(SENSOR_ADDR, 255, 2)
                if maker != b"TI" or int.from_bytes(die, "big") >> 4 != 0x226:
                    raise ValueError("INA226")
                self.sensor_ready = True
            raw = self.bus.readfrom_mem(SENSOR_ADDR, 1, 2)
            value = int.from_bytes(raw, "big")
            if value >= 32768:
                value -= 65536
            amps = value * .0000025 / SHUNT_OHM
            angles = {}
            if profile:
                for key, adc in self.pitch_sensors.items():
                    angles[key] = profile.pitch(key, adc.read_u16())
            return volts, amps, True, angles
        except (OSError, ValueError):
            self.sensor_ready = False
            return volts, 0, False, {}

    def idle_pwm(self):
        self.enable.value(0)
        for output in self.outputs.values():
            output.deinit()
        self.outputs.clear()
        self.last.clear()

    def apply(self, logic):
        if not logic.pwm:
            self.idle_pwm()
        self.power.value(logic.relay)
        if not logic.pwm:
            return
        first_pulse = not self.outputs
        for key, angle in logic.sent.items():
            us = logic.cal.pulse(key, angle)
            if key not in self.outputs:
                output = machine.PWM(machine.Pin(PINS[key]), freq=BAUD_PWM, duty_u16=0)
                self.outputs[key] = output
            if us != self.last.get(key):
                self.outputs[key].duty_ns(us * 1000)
                self.last[key] = us
        if first_pulse:
            time.sleep_ms(4)
        self.enable.value(1)

    def off(self):
        self.enable.value(0)
        self.power.value(0)
        self.idle_pwm()


def load_calibration():
    try:
        with open("calibration.json") as file:
            return Calibration(json.load(file))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def loop():
    board = Board()
    profile = load_calibration()
    logic = Supervisor(profile, time.ticks_diff)
    serial = select.poll()
    serial.register(sys.stdin, select.POLLIN)
    watchdog = machine.WDT(timeout=500)
    buf = ""
    discard = False
    try:
        while True:
            now = time.ticks_ms()
            volts, amps, sensor_ok, angles = board.sample(profile)
            logic.tick(now, bool(board.stop_ok.value()), bool(board.arm.value()),
                       volts, amps, sensor_ok, angles)
            board.apply(logic)
            # Borne la durée d'un traitement même quand le PC envoie en continu.
            for _ in range(48):
                if not serial.poll(0):
                    break
                char = sys.stdin.read(1)
                if not char:
                    break
                if char == "\n":
                    if discard:
                        print("ERR LONGUEUR")
                    else:
                        result = logic.command(buf.rstrip("\r"), time.ticks_ms())
                        board.apply(logic)
                        print(json.dumps(result) if isinstance(result, dict) else result)
                    buf, discard = "", False
                elif len(buf) >= LINE_LIMIT:
                    discard = True
                elif not discard:
                    buf += char
            watchdog.feed()
            time.sleep_ms(5)
    finally:
        board.off()


if __name__ == "__main__":
    loop()
