class BaseVelocityProvider:
    def __init__(self, creature):
        self.creature = creature

    def get_desired_velocity(self):
        raise NotImplementedError
