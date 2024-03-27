import pygame


class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, dy):
        self.rect.y += dy
        self.rect.y = max(0, min(self.rect.y, 1080 - self.rect.height))
