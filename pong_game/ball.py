import pygame
import random


class Ball:
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)
        self.dx = random.choice([-1, 1]) * 14
        self.dy = random.choice([-1, 1]) * 14
