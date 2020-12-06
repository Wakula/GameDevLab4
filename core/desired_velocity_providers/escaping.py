from core.desired_velocity_providers.base import BaseVelocityProvider
import math
import pygame
import random


class AbstractEscaping(BaseVelocityProvider):
    ESCAPE_RADIUS = 150

    def _get_escape_threat_velocity(self, threatening_creature):
        threat_x, threat_y = threatening_creature.bounds.center
        hare_x, hare_y = self.creature.bounds.center
        distance = math.hypot(hare_x-threat_x, hare_y-threat_y)
        if distance <= self.ESCAPE_RADIUS:
            desired_velocity = pygame.Vector2(threat_x-hare_x, threat_y-hare_y)
            if not desired_velocity:
                return pygame.Vector2()
            return desired_velocity.normalize() * self.max_speed * -1
        return pygame.Vector2()

    def get_desired_velocity(self):
        return sum(
            (
                self._get_escape_threat_velocity(creature) for creature in self.creature.other_creatures
                if type(creature) in self.get_threatening_creatures()
            ),
            pygame.Vector2()
        )

    def get_threatening_creatures(self):
        raise NotImplementedError
