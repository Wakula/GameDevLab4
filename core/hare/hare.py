from core.creature import AnimalCreature
from core.common_velocity_providers import Wandering, EdgeEvading
from core.hare.velocity_providers import HareEscaping


class Hare(AnimalCreature):
    VELOCITY_PROVIDERS = (
        EdgeEvading,
        HareEscaping,
        Wandering,
    )
