# TODO: use Wandering, EdgeEvading
# TODO: use ThreatEscaping like
# CREATURES_TO_SEEK = (Hare, FallowDeer, Hunter)
# class WolfSeeking(ThreatEscaping):
#     ESCAPE_RADIUS = 250
#     VELOCITY_MULTIPLIER = 1
#
#     def get_threatening_creatures(self):
#         return CREATURES_TO_SEEK


# class Wolf(AnimalCreature):
#     VELOCITY_PROVIDERS = (
#         Wandering, EdgeEvading, WolfSeeking
#     )
#
#     def update(self, ...):
#         for creature in self.other_creatures:
#             if self.bounds.colliderect(creature) and type(creature) in CREATURES_TO_SEEK:
#                 ...
#         die if not killed for too long
#         super().update(...)
