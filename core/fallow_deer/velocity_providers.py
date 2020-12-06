from core.common_velocity_providers import SeparateEscaping, ThreatEscaping
from core.common_velocity_providers.base import BaseVelocityProvider
from core.hunter.hunter import Hunter
import pygame


class FallowDeerEscaping(ThreatEscaping):
    ESCAPE_RADIUS = 150

    def get_threatening_creatures(self):
        return (Hunter,)


class FallowDeerSeparating(SeparateEscaping):
    ESCAPE_RADIUS = 25
    MIN_FLOCK_SIZE = 3

    def get_flock(self):
        return self.creature.flock

    def get_desired_velocity(self):

        return super().get_desired_velocity()


class FallowDeerFlockSeeking(SeparateEscaping):
    IMPORTANCE_MULTIPLIER = 100
    VELOCITY_MULTIPLIER = 1
    SEEK_RADIUS = 100
    MIN_FLOCK_SIZE = 3

    def _is_velocity_required(self, creature):
        distance = self._get_dist(creature)
        return distance >= self.SEEK_RADIUS

    def get_desired_velocity(self):
        return self.IMPORTANCE_MULTIPLIER * super().get_desired_velocity()

    def get_flock(self):
        return self.creature.flock


class FallowDeerAlign(BaseVelocityProvider):
    def get_desired_velocity(self):
        sum_steering = sum(
            (creature.velocity for creature in self.creature.flock),
            pygame.Vector2()
        )
        sum_steering /= len(self.creature.flock)
        return sum_steering.normalize() * self.creature.max_speed
