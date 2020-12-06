from core.creature import AnimalCreature
from core.common_velocity_providers import EdgeEvading
from core.fallow_deer import velocity_providers


class FallowDeer(AnimalCreature):
    VELOCITY_PROVIDERS = (
        EdgeEvading,
        velocity_providers.FallowDeerFlockSeeking,
        velocity_providers.FallowDeerSeparating,
        velocity_providers.FallowDeerAlign,
        velocity_providers.FallowDeerEscaping,
    )

    def __init__(self, x, y, radius, color, max_speed, max_velocity, max_force, other_creatures):
        super().__init__(x, y, radius, color, max_speed, max_velocity, max_force, other_creatures)
        self.flock = None

    @classmethod
    def create_flock(cls, x, y, radius, color, max_speed, max_velocity, max_force, other_creatures, flock_size):
        flock = []
        for _ in range(flock_size):
            deer = FallowDeer(
                x, y, radius, color, max_speed,
                max_velocity, max_force, other_creatures
            )
            flock.append(deer)
        for deer in flock:
            deer.set_flock(flock)

        return flock

    def set_flock(self, flock):
        self.flock = [deer for deer in flock if deer is not self]
