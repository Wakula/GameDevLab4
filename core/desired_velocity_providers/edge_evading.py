from core.desired_velocity_providers.base import BaseVelocityProvider
import pygame
import settings


class EdgeEvading(BaseVelocityProvider):
    EDGE = 50

    def __init__(self, creature, max_speed):
        super().__init__(creature, max_speed)
        self.x_min = self.EDGE
        self.x_max = settings.SCREEN_WIDTH - self.EDGE

        self.y_min = self.EDGE
        self.y_max = settings.SCREEN_HEIGHT - self.EDGE

    def get_desired_velocity(self):
        x, y = self.creature.bounds.center
        if x > self.x_max:
            desired_x_edge_velocity = pygame.Vector2(-self.max_speed, self.creature.velocity.y)
        elif x < self.x_min:
            desired_x_edge_velocity = pygame.Vector2(self.max_speed, self.creature.velocity.y)
        else:
            desired_x_edge_velocity = pygame.Vector2()
        if y > self.y_max:
            desired_y_edge_velocity = pygame.Vector2(self.creature.velocity.x, -self.max_speed)
        elif y < self.y_min:
            desired_y_edge_velocity = pygame.Vector2(self.creature.velocity.x, self.max_speed)
        else:
            desired_y_edge_velocity = pygame.Vector2()
        return desired_y_edge_velocity + desired_x_edge_velocity
