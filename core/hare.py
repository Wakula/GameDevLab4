from core.creature import Creature
from core.hunter.hunter import Hunter
from core.desired_velocity_providers import Wandering, EdgeEvading, AbstractEscaping
import pygame
import random


class HareEscaping(AbstractEscaping):
    def get_threatening_creatures(self):
        return Hare, Hunter


class Hare(Creature):
    VELOCITY_PROVIDERS = (
        EdgeEvading,
        HareEscaping,
        Wandering,
    )

    def __init__(self, x, y, radius, color, other_creatures):
        super().__init__(x, y, radius, color)
        self.other_creatures = other_creatures
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2(random.random(), random.random()).normalize()
        self.max_speed = 6
        self.max_velocity = 8
        self.max_force = 1
        self.providers = tuple(provider_cls(self, self.max_speed) for provider_cls in self.VELOCITY_PROVIDERS)

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
