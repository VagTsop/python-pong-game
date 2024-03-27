import math
import pygame


class ScrollingBackground:
    def __init__(self, screen, image_path, scroll_speed):
        self.screen = screen
        self.bg = pygame.image.load(image_path).convert()
        self.bg_width = self.bg.get_width()
        self.bg_rect = self.bg.get_rect()
        self.scroll_speed = scroll_speed
        self.tiles = math.ceil(self.screen.get_width() / self.bg_width) + 1
        self.scroll = 0
        self.scrolling_enabled = True  # Flag to control scrolling

    def draw_background(self):
        for i in range(0, self.tiles):
            self.screen.blit(self.bg, (i * self.bg_width + self.scroll, self.bg_rect.y))
            self.bg = pygame.transform.scale(self.bg, (self.bg_width, self.screen.get_height()))

    def scroll_background(self):
        if self.scrolling_enabled:  # Only scroll if enabled
            self.scroll -= self.scroll_speed
            if abs(self.scroll) > self.bg_width:
                self.scroll = 0
        self.draw_background()  # Draw the background regardless of scrolling
