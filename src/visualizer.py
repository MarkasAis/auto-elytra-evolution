import pygame
import sys
import threading
import time

from src.controller import evaluate

pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)


class UpdateThread (threading.Thread):
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
            time.sleep(self.delta_time)


visualisations = []


def visualize(coefficients):
    _, positions = evaluate(coefficients)

    for i in range(len(positions)):
        positions[i] = (positions[i][0], height/3 - (height/100)*positions[i][1])

    visualisations.append((0, positions))


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((255, 255, 255))

    for tick, positions in visualisations:
        pygame.draw.lines(screen, (0, 0, 0), False, positions, 1)

    pygame.display.flip()



render_thread = UpdateThread(2)
render_thread.start()
