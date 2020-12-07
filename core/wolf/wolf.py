from core.common_velocity_providers import Wandering, EdgeEvading
from core.wolf.velocity_providers import WolfSeeking
from core.creature import AnimalCreature 

class Wolf(AnimalCreature):
    VELOCITY_PROVIDERS = (
        Wandering, EdgeEvading, WolfSeeking
    )
    
    def __init__(self, x, y, radius, color, max_speed, max_velocity, max_force, other_creatures, threats, max_hunger):
        super().__init__(x, y, radius, color, max_speed, max_velocity, max_force, other_creatures, threats)
        self.hunger = 0
        self.max_hunger = max_hunger

    def on_collision(self):
        self.hunger = 0

    def update(self):
        self.hunger += 1
        if self.hunger > self.max_hunger:
            self.is_alive = False
        super().update()
    
    def try_kill(self, creature):
        if isinstance(creature, type(self)) or not creature.is_alive or not self.is_alive:
            return
        self.hunger = 0
        creature.is_alive = False
