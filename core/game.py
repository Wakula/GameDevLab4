from collections import defaultdict
from core.hunter.hunter import Hunter
from core.hare import Hare
from core.fallow_deer import FallowDeer
import pygame
import settings
import random


class Game:
    def __init__(self):
        self.game_over = False
        self.players = []
        self.projectiles = []
        pygame.init()
        self.surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.key_down_handlers = defaultdict(list)
        self.key_up_handlers = defaultdict(list)
        self._init_hunter()
        # self._init_hares()
        # self._init_fallow_deer()

    @property
    def objects(self):
        return (*self.players, *self.projectiles)

    def _init_hares(self):
        for _ in range(3):
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(0, settings.SCREEN_HEIGHT)
            hare = Hare(
                x, y,
                settings.HARE_RADIUS,
                settings.HARE_COLOR,
                settings.HARE_MAX_SPEED,
                settings.HARE_MAX_VELOCITY,
                settings.HARE_MAX_FORCE,
                self.players,
            )
            self.players.append(hare)

    def _init_hunter(self):
        x_spawn_position = int((settings.SCREEN_WIDTH - settings.HUNTER_RADIUS) / 2)
        y_spawn_position = settings.SCREEN_HEIGHT - settings.HUNTER_RADIUS * 2
        hunter = Hunter(
            x_spawn_position,
            y_spawn_position,
            settings.HUNTER_RADIUS,
            settings.HUNTER_COLOR,
            settings.HUNTER_SPEED,
            self.projectiles,
        )
        for key in hunter.ALL_KEYS:
            self.key_down_handlers[key].append(hunter.handle_down)
            self.key_up_handlers[key].append(hunter.handle_up)

        self.players.append(hunter)

    def _init_fallow_deer(self):
        x = random.randint(0, settings.SCREEN_WIDTH)
        y = random.randint(0, settings.SCREEN_HEIGHT)
        flock = FallowDeer.create_flock(
            x, y,
            settings.DEER_RADIUS,
            settings.DEER_COLOR,
            settings.DEER_MAX_SPEED,
            settings.DEER_MAX_VELOCITY,
            settings.DEER_MAX_FORCE,
            self.players,
            settings.FLOCK_SIZE,
        )
        self.players += flock

    def handle_projectile_collisions(self):
        collided_projectiles = []
        dead_players = []
        for projectile in self.projectiles:
            for player in self.players:
                if player is projectile.owner:
                    continue
                if player.bounds.colliderect(projectile.bounds):
                    self.on_player_hit(projectile, player, dead_players)
                    collided_projectiles.append(projectile)
            if projectile not in collided_projectiles and projectile.is_out_of_bounds():
                collided_projectiles.append(projectile)
        self.remove_objects(collided_projectiles, dead_players)

    def on_player_hit(self, projectile, player, dead_players):
        projectile.hit(player)
        if player.health <= 0:
            dead_players.append(player)

    def remove_objects(self, collided_projectiles, dead_players):
        for projectile in collided_projectiles:
            self.projectiles.remove(projectile)
        for player in dead_players:
            self.players.remove(player)

    def update(self):
        for game_object in self.objects:
            game_object.update()
        self.handle_projectile_collisions()

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
