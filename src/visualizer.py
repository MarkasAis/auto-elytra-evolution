import pygame
import sys
import threading
import math

from src.controller import evaluate

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

layers = [pygame.Surface((width, height), pygame.SRCALPHA) for i in range(2)]

clock = pygame.time.Clock()

player_scale = 0.1
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (player.get_width() * player_scale, player.get_height() * player_scale))

background = pygame.image.load("background.png")

RESOLUTION = 5

best_fitness = -math.inf


def lerp(start, end, t):
    return (end-start) * t + start


def lerp_color(start, end, t):
    return tuple(lerp(start[i], end[i], t) for i in range(len(start)))

class Visualisation():
    def __init__(self, coefficients, resolution=5):
        self.cur_color = None
        self.cur_width = None

        self.tick = 1
        self.positions = []

        self.fade_ticks = 50

        self.fitness, positions = evaluate(coefficients)
        for i in range(0, len(positions), resolution):
            self.positions.append((positions[i][0], height / 5 - (height / 100) * positions[i][1]))

        global best_fitness
        if self.fitness > best_fitness:
            best_fitness = self.fitness

    @property
    def in_progress(self):
        return self.tick < len(self.positions)

    @property
    def is_finished(self):
        return self.cur_color is not None and self.cur_color[3] <= 5

    @property
    def is_best(self):
        return self.fitness >= best_fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def compute_color(self):
        alpha = clamp(1 - (self.tick - len(self.positions)) / self.fade_ticks, 0, 1) * 200

        if self.is_best:
            return 255, 50, 150, alpha

        return 255, 255, 255, alpha

    def compute_width(self):
        return 4 if self.is_best else 2


    def update_style(self):
        # color
        target_color = self.compute_color()
        if self.cur_color is None:
            self.cur_color = target_color
        self.cur_color = lerp_color(self.cur_color, target_color, 0.05)

        # width
        target_width = self.compute_width()
        if self.cur_width is None:
            self.cur_width = target_width
        self.cur_width = lerp(self.cur_width, target_width, 0.05)

    def update(self):
        if self.is_finished:
            return

        self.update_style()

        num_positions = min(len(self.positions), self.tick)
        pygame.draw.lines(layers[0], self.cur_color, False, self.positions[0:num_positions + 1], int(self.cur_width))

        if self.in_progress:
            prev_pos = self.positions[num_positions - 2]
            cur_pos = self.positions[num_positions - 1]

            dx = prev_pos[0] - cur_pos[0]
            dy = prev_pos[1] - cur_pos[1]
            angle = 90 - math.atan2(dy, dx) * 180 / math.pi

            blitRotate(layers[1], player, cur_pos, (player.get_width() / 2, player.get_height() / 2), angle)

        self.tick = self.tick + 1


visualisations = []


def visualize(coefficients):
    # _, positions = evaluate(coefficients)
    #
    # vis_positions = []
    #
    # for i in range(0, len(positions), RESOLUTION):
    #     vis_positions.append((positions[i][0], height / 5 - (height / 100) * positions[i][1]))
    #
    # visualisations.append([0, vis_positions])
    #
    visualisations.append(Visualisation(coefficients, RESOLUTION))


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
    global visualisations

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for layer in layers:
        layer.fill((0, 0, 0, 0))

    cur_visualisations = sorted(visualisations.copy())

    for vis in cur_visualisations:
        vis.update()
        if vis.is_finished:
            visualisations.remove(vis)

    # visualisations = next_visualisations

    screen.blit(background, (0, 0))

    for layer in layers:
        screen.blit(layer, (0, 0))

    pygame.display.flip()


# render_thread = UpdateThread(60)
# render_thread.start()

def run():
    while True:
        update()
        # time.sleep(self.delta_time)
        clock.tick(60)
