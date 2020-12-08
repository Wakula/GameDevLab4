from collections import defaultdict
from core.hunter.hunter import Hunter
from core.hare import Hare
from core.wolf.wolf import Wolf
from core.fallow_deer import FallowDeer
from core.creature import AnimalCreature
import pygame
import settings
import random
import core.config as config


class Game:
    def __init__(self):
        self.game_over = False
        self.creatures = []
        self.projectiles = []
        pygame.init()
        self.surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.key_down_handlers = defaultdict(list)
        self.key_up_handlers = defaultdict(list)
        self._init_hunter()
        self._init_hares()
        self._init_fallow_deer()
        self._init_wolves()

    @property
    def objects(self):
        return (*self.creatures, *self.projectiles)

    def _init_hares(self):
        for _ in range(config.HARE_COUNT):
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(0, settings.SCREEN_HEIGHT)
            hare = Hare(
                x, y,
                settings.HARE_RADIUS,
                settings.HARE_COLOR,
                settings.HARE_MAX_SPEED,
                settings.HARE_MAX_VELOCITY,
                settings.HARE_MAX_FORCE,
                self.creatures,
                (Hare, Wolf, Hunter, FallowDeer)
            )
            self.creatures.append(hare)

    def _init_hunter(self):
        x_spawn_position = int((settings.SCREEN_WIDTH - settings.HUNTER_RADIUS) / 2)
        y_spawn_position = settings.SCREEN_HEIGHT - settings.HUNTER_RADIUS * 2
        hunter = Hunter(
            x_spawn_position,
            y_spawn_position,
            settings.HUNTER_RADIUS,
            settings.HUNTER_COLOR,
            settings.HUNTER_SPEED,
            self.projectiles
        )
        for key in hunter.ALL_KEYS:
            self.key_down_handlers[key].append(hunter.handle_down)
            self.key_up_handlers[key].append(hunter.handle_up)

        self.creatures.append(hunter)

    def _init_fallow_deer(self):
        for _ in range(config.DEER_FLOCKS):
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(0, settings.SCREEN_HEIGHT)
            flock = FallowDeer.create_flock(
                x, y,
                settings.DEER_RADIUS,
                settings.DEER_COLOR,
                settings.DEER_MAX_SPEED,
                settings.DEER_MAX_VELOCITY,
                settings.DEER_MAX_FORCE,
                self.creatures,
                (Hunter,),
                (Wolf,),
                config.FLOCK_SIZE
            )
            self.creatures += flock.creatures

    def _init_wolves(self):
        for _ in range(config.WOLF_COUNT):
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(0, settings.SCREEN_HEIGHT)
            hare = Wolf(
                x, y,
                settings.WOLF_RADIUS,
                settings.WOLF_COLOR,
                settings.WOLF_MAX_SPEED,
                settings.WOLF_MAX_VELOCITY,
                settings.WOLF_MAX_FORCE,
                self.creatures,
                (Hare, Hunter, FallowDeer),
                settings.WOLF_HUNGER
            )
            self.creatures.append(hare)

    def handle_projectile_collisions(self):
        collided_projectiles = []
        for projectile in self.projectiles:
            if projectile.lifetime <= 0:
                collided_projectiles.append(projectile)
                continue

            for creature in self.creatures:
                if creature is projectile.owner:
                    continue
                if creature.bounds.colliderect(projectile.bounds):
                    creature.is_alive = False
                    collided_projectiles.append(projectile)
            if projectile not in collided_projectiles and projectile.is_out_of_bounds():
                collided_projectiles.append(projectile)
        
        self.remove_creatures()
        self.remove_projectiles(collided_projectiles)

    def handle_creature_collisions(self):
        for creature1 in self.creatures:
            for creature2 in self.creatures:
                if creature1.bounds.colliderect(creature2.bounds) and isinstance(creature1, AnimalCreature):
                    creature1.try_kill(creature2)

        self.remove_creatures()

    def remove_creatures(self):
        dead_creatures = filter(lambda c: not c.is_alive, self.creatures)
        for creature in dead_creatures:
            creature.on_killed()
            self.creatures.remove(creature)

    def remove_projectiles(self, collided_projectiles):
        for projectile in collided_projectiles:
            self.projectiles.remove(projectile)

    def update(self):
        for game_object in self.objects:
            game_object.update()

        self.handle_projectile_collisions()
        self.handle_creature_collisions()

    def draw(self):
        for game_object in self.objects:
            game_object.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                for handler in self.key_down_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.key_up_handlers[event.key]:
                    handler(event.key)

    def run(self):
        while not self.game_over:
            self.surface.fill(settings.BACKGROUND_COLOR)
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(settings.FRAME_RATE)
