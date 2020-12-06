from core.game_object import GameObject
import pygame


class Creature(GameObject):
    def __init__(self, x, y, radius, color):
        self.radius = radius
        self.diameter = 2 * radius
        self.color = color
        super().__init__(x - radius, y - radius, self.diameter, self.diameter)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.bounds.center, self.radius)

    def move(self, dx, dy):
        super().move(dx, dy)
