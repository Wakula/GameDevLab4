from core.hunter.hunter import Hunter
from core.fallow_deer.fallow_deer import FallowDeer
from core.wolf.wolf import Wolf
from core.common_velocity_providers import ThreatEscaping


class HareEscaping(ThreatEscaping):
    ESCAPE_RADIUS = 150
