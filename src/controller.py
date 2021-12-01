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


def denormalize(coefficients):
    descent_angle = coefficients[0] * 10 + 45
    max_descent_speed = coefficients[1] * 1 + 1
    descent_pitch_speed = coefficients[2] * 1 + 1
    ascent_angle = coefficients[3] * 10 - 45
    min_ascent_speed = coefficients[4] * 1 + 1
    ascent_pitch_speed = coefficients[5] * 1 + 5

    return descent_angle, max_descent_speed, descent_pitch_speed, ascent_angle, min_ascent_speed, ascent_pitch_speed


def evaluate(coefficients):
    descent_angle, max_descent_speed, descent_pitch_speed, ascent_angle, min_ascent_speed, ascent_pitch_speed = denormalize(
        coefficients)
    emulator = ElytraEmulator()

    is_descending = True
    score = 0
    positions = []

    for i in range(1000):
        if is_descending and emulator.speed >= max_descent_speed:
            is_descending = False
        elif not is_descending and emulator.speed <= min_ascent_speed:
            is_descending = True

        if is_descending:
            pitch_towards_angle(emulator, descent_angle, descent_pitch_speed)
        else:
            pitch_towards_angle(emulator, ascent_angle, ascent_pitch_speed)

        emulator.tick()

        score += emulator.position.y
        x = emulator.position.horizontal_length
        y = emulator.position.y
        positions.append((x, y))

    return score, positions
