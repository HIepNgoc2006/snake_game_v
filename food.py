import random
import math
import pygame


class Food:
    def __init__(self, screen_width, screen_height, snake_size, food_size, sprite):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake_size = snake_size
        self.food_size = food_size
        self.sprite = sprite
        self.pos = self._random_pos()
        self.spawn = True

    def _random_pos(self):
        return [
            random.randrange(0, (self.screen_width - self.food_size) // self.snake_size)
            * self.snake_size,
            random.randrange(0, (self.screen_height - self.food_size) // self.snake_size)
            * self.snake_size,
        ]

    def respawn(self, snake_body):
        # Keep generating until it doesn't overlap the snake
        while True:
            pos = self._random_pos()
            food_on_snake = False
            for segment in snake_body:
                if (
                    pos[0] < segment[0] + self.snake_size
                    and pos[0] + self.food_size > segment[0]
                    and pos[1] < segment[1] + self.snake_size
                    and pos[1] + self.food_size > segment[1]
                ):
                    food_on_snake = True
                    break
            if not food_on_snake:
                self.pos = pos
                break
        self.spawn = True

    def draw(self, surface, wave_phase=0, wave_amplitude=0):
        surface.blit(self.sprite, (self.pos[0], self.pos[1] - wave_amplitude * math.sin(wave_phase)))
