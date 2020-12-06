import random
import math
import pygame
from core.common_velocity_providers.base import BaseVelocityProvider


class Wandering(BaseVelocityProvider):
    CIRCLE_DISTANCE = 50
    CIRCLE_RADIUS = 25
    ANGLE_DELTA = 15

    def __init__(self, creature):
        super().__init__(creature)
        self.angle = 0

    def get_desired_velocity(self):
        if random.random() > 0.5:
            self.angle += self.ANGLE_DELTA
        else:
            self.angle -= self.ANGLE_DELTA
        vector_to_circle = self.creature.velocity.normalize() * self.CIRCLE_DISTANCE
        creature_x, creature_y = self.creature.bounds.center
        circle_x, circle_y = creature_x + vector_to_circle.x, creature_y + vector_to_circle.y
        vector_from_circle_to_target = pygame.Vector2(math.sin(self.angle), math.cos(self.angle)) * self.CIRCLE_RADIUS
        target_x, target_y = circle_x + vector_from_circle_to_target.x, circle_y + vector_from_circle_to_target.y
        return pygame.Vector2(target_x-creature_x, target_y-creature_y).normalize() * self.creature.max_speed
