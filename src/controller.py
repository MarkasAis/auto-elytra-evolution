import math

from src.emulator import ElytraEmulator


def pitch_towards_angle(emulator, angle, speed):
    angle_difference = angle - emulator.pitch
    direction = math.copysign(1, angle_difference)

    if abs(angle_difference) < speed:
        emulator.pitch = angle
        return True

    emulator.pitch += direction * speed
    return False


def evaluate(descent_angle, max_descent_speed, descent_pitch_speed, ascent_angle, min_ascent_speed, ascent_pitch_speed):
    emulator = ElytraEmulator()

    is_descending = True
    score = 0
    altitudes = []

    for i in range(1000):
        if is_descending and emulator.speed >= max_descent_speed:
            is_descending = False
        elif not is_descending and emulator.speed <= min_ascent_speed:
            is_descending = True

        if is_descending:
            pitch_towards_angle(emulator, descent_angle, descent_pitch_speed)
        else:
            pitch_towards_angle(emulator, ascent_angle, ascent_pitch_speed)

        score += emulator.position.y
        altitudes.append(emulator.position.y)

    return score, altitudes
