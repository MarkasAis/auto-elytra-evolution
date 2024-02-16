import pygame
import sys
import math

from controller import evaluate

pygame.init()
clock = pygame.time.Clock()
delta_time = 0

size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Poggies! :)')
layers = [pygame.Surface((width, height), pygame.SRCALPHA) for i in range(2)]

player_scale = 0.15
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (player.get_width() * player_scale, player.get_height() * player_scale))

background = pygame.image.load("background.png")

RESOLUTION = 10
best_fitness = -math.inf


def lerp(start, end, t):
    return (end-start) * t + start


def lerp_vec(start, end, t):
    return tuple(lerp(start[i], end[i], t) for i in range(len(start)))


class Visualisation():
    def __init__(self, coefficients, resolution=5):
        self.cur_color = None
        self.cur_width = None

        self.tick = 1
        self.positions = []

        self.fade_ticks = 30

        self.fitness, positions = evaluate(coefficients)
        for i in range(0, len(positions), resolution):
            self.positions.append((positions[i][0] * 2, height / 5 - (height / 100) * positions[i][1]))

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
        alpha = clamp(1 - (self.tick - len(self.positions)) / self.fade_ticks, 0, 1)

        if self.is_best:
            return 228, 63, 110, alpha * 255

        return 255, 255, 255, alpha * 200

    def compute_width(self):
        return 5 if self.is_best else 3

    def update_style(self):
        # color
        target_color = self.compute_color()
        if self.cur_color is None:
            self.cur_color = target_color
        self.cur_color = lerp_vec(self.cur_color, target_color, 0.5)

        # width
        target_width = self.compute_width()
        if self.cur_width is None:
            self.cur_width = target_width
        self.cur_width = lerp(self.cur_width, target_width, 0.05)

    def update(self):
        if self.is_finished:
            return

        self.update_style()

        num_positions = min(len(self.positions), math.ceil(self.tick))
        num_positions_2 = min(len(self.positions), math.floor(self.tick))

        if num_positions_2 > 2:
            pygame.draw.lines(layers[0], self.cur_color, False, self.positions[0:num_positions_2], int(self.cur_width))

        if self.in_progress:
            prev_pos = self.positions[num_positions - 2]
            cur_pos = self.positions[num_positions - 1]

            frac, _ = math.modf(self.tick)

            pos = lerp_vec(prev_pos, cur_pos, frac)

            dx = prev_pos[0] - cur_pos[0]
            dy = prev_pos[1] - cur_pos[1]
            angle = 90 - math.atan2(dy, dx) * 180 / math.pi

            blit_rotate(layers[1], player, pos, (player.get_width() / 2, player.get_height() / 2), angle)

        self.tick = self.tick + 10*delta_time


visualisations = []


def visualize(coefficients):
    visualisations.append(Visualisation(coefficients, RESOLUTION))


def blit_rotate(surf, image, pos, origin_pos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - origin_pos[0], pos[1] - origin_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # rotated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


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

    screen.blit(background, (0, 0))

    for layer in layers:
        screen.blit(layer, (0, 0))

    from evolution import get_generation_count

    color = (255, 255, 255)

    font = pygame.font.SysFont(None, 50)
    img = font.render('GENERATION', True, color)
    screen.blit(img, (width / 2 - img.get_width() / 2, 100 - img.get_height() / 2))

    font = pygame.font.SysFont(None, 150)
    img = font.render(str(get_generation_count()), True, color)
    screen.blit(img, (width / 2 - img.get_width() / 2, 175 - img.get_height() / 2))

    pygame.display.flip()


def run():
    global delta_time

    while True:
        update()
        delta_time = clock.tick(30) / 1000
