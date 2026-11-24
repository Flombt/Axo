"""MicroPython sur RP2040. Le premier démarrage ne commande aucun moteur."""
from machine import Pin, PWM, WDT
from select import poll, POLLIN
from sys import stdin
from time import sleep_ms, ticks_add, ticks_diff, ticks_ms

from controle import AXES, BOUNDS, Motion, PERIOD_MS, pulse_us

PINS = (6, 7, 8, 9, 10, 11)
# Remplir les six tuples avant de mettre COMMISSIONED à True.
# Chaque tuple contient le neutre (µs), la pente signée (µs/° moteur),
# puis les deux limites d'impulsion mesurées sur ce servo.
PROFILE = ()
COMMISSIONED = False
MAX_LINE = 96


def commissioning_ok():
    if not COMMISSIONED or len(PROFILE) != len(AXES):
        return False
    try:
        for i, limits in enumerate(BOUNDS):
            neutral, slope, low, high = PROFILE[i]
            if not (500 <= low < neutral < high <= 2500 and 0 < abs(slope) < 30):
                return False
            for q in (*limits, 0):
                pulse_us(q, i, PROFILE)
    except (TypeError, ValueError):
        return False
    return True


def main():
    machine = Motion(commissioning_ok())
    pwm = []
    for number in PINS:
        pin = Pin(number, Pin.OUT, value=0)
        channel = PWM(pin, freq=50, duty_u16=0)
        pwm.append(channel)
    watchdog = WDT(timeout=1400)
    input_events = poll()
    input_events.register(stdin, POLLIN)
    line = ""
    overflow = False
    due = ticks_ms()
    while True:
        for _ in range(48):
            if not input_events.poll(0):
                break
            ch = stdin.read(1)
            if not ch:
                break
            if ch == "\n":
                try:
                    if overflow:
                        raise ValueError("ligne trop longue")
                    command = machine.command(line, ticks_ms())
                    print("OK", command, int(machine.armed), machine.reason)
                except ValueError as exc:
                    print("ERR", str(exc))
                line = ""
                overflow = False
            elif ch != "\r":
                if len(line) < MAX_LINE:
                    line += ch
                else:
                    overflow = True
        now = ticks_ms()
        if ticks_diff(now, due) >= 0:
            due = ticks_add(now, PERIOD_MS)
            state = machine.tick(now, ticks_diff)
            try:
                us = [pulse_us(v, i, PROFILE) for i,v in enumerate(state)] if state else None
            except ValueError:
                machine.stop("limite impulsion")
                us = None
            for i, channel in enumerate(pwm):
                channel.duty_ns(us[i] * 1000 if us else 0)
        watchdog.feed()
        sleep_ms(1)


main()
