class BaseVelocityProvider:
    def __init__(self, creature, max_speed):
        self.max_speed = max_speed
        self.creature = creature

    def get_desired_velocity(self):
        raise NotImplementedError
