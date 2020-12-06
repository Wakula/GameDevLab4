from core.creature import Creature
import pygame
import settings
import math


class Hare(Creature):
    def __init__(self, x, y, radius, color, other_creatures, player):
        # TODO: just for test remove soon
        self.player = player
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2()

        self.max_speed = 6
        self.max_force = 5
        super().__init__(x, y, radius, color)

    @property
    def desired_escape_velocity(self):
        hunter_escape_radius = 150
        hunter_x, hunter_y = self.player.bounds.center
        hare_x, hare_y = self.bounds.center
        distance = math.hypot(hare_x-hunter_x, hare_y-hunter_y)
        if distance <= hunter_escape_radius:
            target_x, target_y = self.player.bounds.center
            location_x, location_y = self.bounds.center
            desired = pygame.Vector2(target_x-location_x, target_y-location_y)
            return desired.normalize() * self.max_speed * -1
        return pygame.Vector2()

    @property
    def desired_out_of_bounds_velocity(self):
        edge = 20
        x, y = self.bounds.center
        if x > settings.SCREEN_WIDTH - edge:
            return pygame.Vector2(-self.max_speed, self.velocity.y)
        if x < edge:
            return pygame.Vector2(self.max_speed, self.velocity.y)
        if y > settings.SCREEN_HEIGHT - edge:
            return pygame.Vector2(self.velocity.x, -self.max_speed)
        if y < edge:
            return pygame.Vector2(self.velocity.x, self.max_speed)
        return pygame.Vector2()

    def update(self):
        desired_velocity = self.desired_escape_velocity + 3 * self.desired_out_of_bounds_velocity
        steer = desired_velocity - self.velocity
        # print(steer.magnitude() * 100)
        if steer.magnitude() > self.max_force:
            # print(steer.magnitude())
            steer = steer.normalize() * self.max_force
        self.apply_force(steer)
        self.velocity += self.acceleration
        self.acceleration = pygame.Vector2()
        self.move(*self.velocity)

    def apply_force(self, force):
        self.acceleration += force
