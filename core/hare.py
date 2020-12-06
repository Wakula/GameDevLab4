from core.creature import AnimalCreature
from core.hunter.hunter import Hunter
from core.fallow_deer.fallow_deer import FallowDeer
from core.common_velocity_providers import Wandering, EdgeEvading, ThreatEscaping


class HareEscaping(ThreatEscaping):
    ESCAPE_RADIUS = 150

    def get_threatening_creatures(self):
        return Hare, Hunter, FallowDeer


class Hare(AnimalCreature):
    VELOCITY_PROVIDERS = (
        EdgeEvading,
        HareEscaping,
        Wandering,
    )
