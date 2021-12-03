import pygame
import sys
import threading
import math

from src.controller import evaluate

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

player_scale = 0.1
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (player.get_width() * player_scale, player.get_height() * player_scale))

background = pygame.image.load("background.png")

foreground = pygame.Surface((width, height), pygame.SRCALPHA)


class UpdateThread(threading.Thread):
    def __init__(self, frames_per_second):
        threading.Thread.__init__(self)
        self.frames_per_second = frames_per_second
        self.delta_time = 1 / frames_per_second
        self.active = True

    def stop(self):
        self.active = False

    def run(self):
        while self.active:
            update()
            # time.sleep(self.delta_time)
            clock.tick(self.frames_per_second)


visualisations = []


def visualize(coefficients, resolution=5):
    _, positions = evaluate(coefficients)

    vis_positions = []

    for i in range(0, len(positions), resolution):
        vis_positions.append((positions[i][0], height / 5 - (height / 100) * positions[i][1]))

    visualisations.append([0, vis_positions])


def blitRotate(surf, image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def update():
    # print("tick")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # screen.fill((255, 255, 255))

    screen.blit(background, (0, 0))

    foreground.fill((0, 0, 0, 0))

    for i in range(len(visualisations) - 1, -1, -1):
        tick, positions = visualisations[i]

        num_positions = min(len(positions), tick)
        in_progress = num_positions < len(positions)

        alpha = clamp(1 - (tick - len(positions)) * 0.01, 0, 1) * 200
        color = (255, 255, 255, alpha)

        if alpha <= 0:
            visualisations.remove(visualisations[i])
            continue

        if num_positions > 1:
            pygame.draw.lines(foreground, color, False, positions[0:num_positions], 2)

            if in_progress:
                prev_pos = positions[num_positions - 2]
                cur_pos = positions[num_positions - 1]
                # screen.blit(player, last_pos)

                dx = prev_pos[0] - cur_pos[0]
                dy = prev_pos[1] - cur_pos[1]

                angle = 90 - math.atan2(dy, dx) * 180 / math.pi

                blitRotate(foreground, player, cur_pos, (player.get_width() / 2, player.get_height() / 2), angle)

        visualisations[i][0] += 1

    # draw_polygon_alpha(screen, (255, 255, 0, 127),
    #                    [(100, 10), (100 + 0.8660 * 90, 145), (100 - 0.8660 * 90, 145)])

    screen.blit(foreground, (0, 0))

    pygame.display.flip()


# render_thread = UpdateThread(60)
# render_thread.start()

def run():
    while True:
        update()
        # time.sleep(self.delta_time)
        clock.tick(60)
