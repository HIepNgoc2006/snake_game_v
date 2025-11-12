import pygame


class Snake:
    def __init__(self, init_pos, size, speed, head_sprite, body_sprite):
        self.pos = list(init_pos)
        self.size = size
        self.speed = speed
        # initialize a small body aligned on the left
        self.body = [list(init_pos), [init_pos[0] - size, init_pos[1]], [init_pos[0] - 2 * size, init_pos[1]]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.head_sprite = head_sprite
        self.body_sprite = body_sprite

    def update_direction(self):
        self.direction = self.change_to

    def move(self):
        if self.direction == "UP":
            self.pos[1] -= self.speed
        elif self.direction == "DOWN":
            self.pos[1] += self.speed
        elif self.direction == "LEFT":
            self.pos[0] -= self.speed
        elif self.direction == "RIGHT":
            self.pos[0] += self.speed

        # grow by inserting head position; popping handled by caller when not eating
        self.body.insert(0, list(self.pos))

    def shrink_tail(self):
        # remove last segment (call when no food eaten)
        if self.body:
            self.body.pop()

    def draw(self, surface):
        # Draw body (excluding head)
        for pos in self.body[1:]:
            surface.blit(self.body_sprite, (pos[0], pos[1]))
        # Draw head
        surface.blit(self.head_sprite, (self.pos[0], self.pos[1]))

    def check_self_collision(self):
        for block in self.body[1:]:
            if self.pos[0] == block[0] and self.pos[1] == block[1]:
                return True
        return False

    def check_wall_collision(self, screen_width, screen_height):
        if self.pos[0] < 0 or self.pos[0] > screen_width - self.size:
            return True
        if self.pos[1] < 0 or self.pos[1] > screen_height - self.size:
            return True
        return False
