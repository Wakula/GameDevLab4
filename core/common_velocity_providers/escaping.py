import pygame
from core.common_velocity_providers.base import BaseVelocityProvider
import math


# TODO: maybe there is a way to somehow make this a general class for Escaping/Seeking
class AbstractEscaping(BaseVelocityProvider):
    ESCAPE_RADIUS = None
    VELOCITY_MULTIPLIER = -1

    def _get_dist(self, creature):
        escape_x, escape_y = creature.bounds.center
        creature_x, creature_y = self.creature.bounds.center
        return math.hypot(creature_x - escape_x, creature_y - escape_y)

    def _is_velocity_required(self, creature):
        distance = self._get_dist(creature)
        return distance <= self.ESCAPE_RADIUS

    def _get_escape_velocity(self, escape_creature):
        escape_x, escape_y = escape_creature.bounds.center
        creature_x, creature_y = self.creature.bounds.center
        if self._is_velocity_required(escape_creature):
            desired_velocity = pygame.Vector2(escape_x-creature_x, escape_y-creature_y)
            if not desired_velocity:
                return pygame.Vector2()
            return desired_velocity.normalize() * self.get_desired_distance() * self.VELOCITY_MULTIPLIER
        return pygame.Vector2()

    def get_desired_velocity(self):
        raise NotImplementedError

    def get_desired_distance(self):
        raise NotImplementedError


class ThreatEscaping(AbstractEscaping):
    def get_desired_velocity(self):
        return sum(
            (
                self._get_escape_velocity(creature) for creature in self.creature.other_creatures
                if type(creature) in self.get_threatening_creatures()
            ),
            pygame.Vector2()
        )

    def get_threatening_creatures(self):
        raise NotImplementedError

    def get_desired_distance(self):
        return self.creature.max_speed


class SeparateEscaping(AbstractEscaping):
    MIN_FLOCK_SIZE = None

    def get_desired_velocity(self):

        flock = self.get_flock()
        if len(flock.creatures) < self.MIN_FLOCK_SIZE - 1:
            return pygame.Vector2()

        return sum(
            (
                self._get_escape_velocity(creature) for creature in flock.creatures
            ),
            pygame.Vector2()
        )

    def get_flock(self):
        raise NotImplementedError

    def get_desired_distance(self):
        return self.creature.radius * 2

    def _get_escape_velocity(self, escape_creature):
        velocity = super()._get_escape_velocity(escape_creature)
        if velocity:
            velocity /= self._get_dist(escape_creature)
        return velocity
