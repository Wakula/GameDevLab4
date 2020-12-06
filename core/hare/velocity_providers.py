from core.hunter.hunter import Hunter
from core.fallow_deer.fallow_deer import FallowDeer
from core.common_velocity_providers import ThreatEscaping


class HareEscaping(ThreatEscaping):
    ESCAPE_RADIUS = 150

    def get_threatening_creatures(self):
        return self.creature.__class__, Hunter, FallowDeer
