from core.game_object import GameObject
import pygame
import random


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


class AnimalCreature(Creature):
    VELOCITY_PROVIDERS = None

    def __init__(self, x, y, radius, color, max_speed, max_velocity, max_force, other_creatures):
        super().__init__(x, y, radius, color)
        self.other_creatures = other_creatures
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2(random.random(), random.random()).normalize()
        self.max_speed = max_speed
        self.max_velocity = max_velocity
        self.max_force = max_force
        self.providers = self._get_providers()

    def _get_providers(self):
        return tuple(provider_cls(self) for provider_cls in self.VELOCITY_PROVIDERS)

    def update(self):
        desired_velocity = sum(
            (provider.get_desired_velocity() for provider in self.providers),
            pygame.Vector2()
        )
        steer = desired_velocity - self.velocity
        if steer.magnitude() > self.max_force:
            steer = steer.normalize() * self.max_force
        self.acceleration += steer
        self.velocity += self.acceleration
        if self.velocity.magnitude() > self.max_velocity:
            self.velocity = self.velocity.normalize() * self.max_velocity
        self.move(*self.velocity)
        self.acceleration = pygame.Vector2()
