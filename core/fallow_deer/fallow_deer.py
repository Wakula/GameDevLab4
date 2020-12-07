from core.creature import AnimalCreature, Flock
from core.common_velocity_providers import EdgeEvading
from core.fallow_deer import velocity_providers


class FallowDeer(AnimalCreature):
    VELOCITY_PROVIDERS = (
        EdgeEvading,
        velocity_providers.FallowDeerFlockSeeking,
        velocity_providers.FallowDeerSeparating,
        velocity_providers.FallowDeerAlign,
        velocity_providers.FallowDeerEscaping,
        velocity_providers.FallowDeerWolfEscaping
    )

    def __init__(self, x, y, radius, color, max_speed, max_velocity, max_force, other_creatures, threats, special_threats):
        super().__init__(x, y, radius, color, max_speed, max_velocity, max_force, other_creatures, threats)
        self.flock = None
        self.special_threats = special_threats

    @classmethod
    def create_flock(cls, x, y, radius, color, max_speed, max_velocity, max_force, other_creatures, threats, special_threats, flock_size):
        flock = Flock()
        for _ in range(flock_size):
            deer = FallowDeer(
                x, y, radius, color, max_speed,
                max_velocity, max_force, other_creatures,
                threats, special_threats
            )
            flock.add_creature(deer)

        return flock
    
    def on_killed(self):
        self.flock.remove_creature(self)