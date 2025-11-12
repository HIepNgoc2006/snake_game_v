import pygame
import random


class Obstacle:
    """Represents a single obstacle block"""
    def __init__(self, x, y, size, color=(139, 69, 19)):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.border_color = (101, 50, 10)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)


class Portal:
    """Portal that appears after eating enough food"""
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size * 2, size * 2)
        self.color = (255, 215, 0)  # Gold color
        self.glow_color = (255, 255, 0)
        self.active = False
        self.animation_phase = 0
    
    def activate(self):
        self.active = True
    
    def update(self):
        if self.active:
            self.animation_phase = (self.animation_phase + 0.1) % (2 * 3.14159)
    
    def draw(self, surface):
        if self.active:
            # Animated glow effect
            glow_size = int(5 + 3 * abs(pygame.math.Vector2(1, 0).rotate(self.animation_phase * 57.3).x))
            glow_rect = self.rect.inflate(glow_size, glow_size)
            pygame.draw.rect(surface, self.glow_color, glow_rect, 3)
            pygame.draw.rect(surface, self.color, self.rect)
            
            # Draw portal symbol
            center = self.rect.center
            pygame.draw.circle(surface, (0, 0, 0), center, 8)
            pygame.draw.circle(surface, self.glow_color, center, 6, 2)


class LevelManager:
    """Manages obstacles and portals for campaign mode"""
    def __init__(self, screen_width, game_area_height, snake_size):
        self.screen_width = screen_width
        self.game_area_height = game_area_height
        self.snake_size = snake_size
        self.current_level = 1
        self.max_levels = 5
        self.obstacles = []
        self.portal = None
        self.food_eaten_this_level = 0
        self.food_required_for_portal = 20
        
    def start_level(self, level):
        """Initialize obstacles for the given level"""
        self.current_level = level
        self.food_eaten_this_level = 0
        self.obstacles = []
        self.portal = None
        
        # Create obstacles based on level
        if level == 1:
            # Level 1: Simple walls
            self._create_horizontal_wall(self.screen_width // 2 - 60, self.game_area_height // 2, 6)
        
        elif level == 2:
            # Level 2: Cross pattern
            self._create_horizontal_wall(self.screen_width // 2 - 60, self.game_area_height // 2, 6)
            self._create_vertical_wall(self.screen_width // 2, self.game_area_height // 2 - 60, 6)
        
        elif level == 3:
            # Level 3: Four corners
            self._create_horizontal_wall(40, 100, 4)
            self._create_horizontal_wall(self.screen_width - 120, 100, 4)
            self._create_horizontal_wall(40, self.game_area_height - 120, 4)
            self._create_horizontal_wall(self.screen_width - 120, self.game_area_height - 120, 4)
        
        elif level == 4:
            # Level 4: Maze-like
            self._create_horizontal_wall(60, 150, 5)
            self._create_horizontal_wall(self.screen_width - 160, 150, 5)
            self._create_horizontal_wall(60, self.game_area_height - 150, 5)
            self._create_horizontal_wall(self.screen_width - 160, self.game_area_height - 150, 5)
            self._create_vertical_wall(self.screen_width // 2, 100, 8)
        
        elif level == 5:
            # Level 5: Complex pattern (hardest)
            self._create_horizontal_wall(40, 120, 8)
            self._create_horizontal_wall(40, self.game_area_height - 140, 8)
            self._create_vertical_wall(80, 120, 6)
            self._create_vertical_wall(self.screen_width - 80, 120, 6)
            self._create_horizontal_wall(self.screen_width // 2 - 60, self.game_area_height // 2, 6)
            self._create_vertical_wall(self.screen_width // 2, self.game_area_height // 2 - 80, 8)
    
    def _create_horizontal_wall(self, x, y, length):
        """Create a horizontal wall of obstacles"""
        for i in range(length):
            obs = Obstacle(x + i * self.snake_size, y, self.snake_size)
            self.obstacles.append(obs)
    
    def _create_vertical_wall(self, x, y, length):
        """Create a vertical wall of obstacles"""
        for i in range(length):
            obs = Obstacle(x, y + i * self.snake_size, self.snake_size)
            self.obstacles.append(obs)
    
    def on_food_eaten(self):
        """Called when snake eats food"""
        self.food_eaten_this_level += 1
        
        # Activate portal after eating required amount
        if self.food_eaten_this_level >= self.food_required_for_portal and not self.portal:
            self._spawn_portal()
    
    def _spawn_portal(self):
        """Spawn the portal at a safe location"""
        # Find a safe spot not occupied by obstacles
        attempts = 0
        while attempts < 100:
            x = random.randint(2, (self.screen_width // self.snake_size) - 4) * self.snake_size
            y = random.randint(2, (self.game_area_height // self.snake_size) - 4) * self.snake_size
            
            portal_rect = pygame.Rect(x, y, self.snake_size * 2, self.snake_size * 2)
            
            # Check if position is clear
            is_clear = True
            for obs in self.obstacles:
                if portal_rect.colliderect(obs.rect):
                    is_clear = False
                    break
            
            if is_clear:
                self.portal = Portal(x, y, self.snake_size)
                self.portal.activate()
                break
            
            attempts += 1
    
    def check_obstacle_collision(self, rect):
        """Check if rect collides with any obstacle"""
        for obs in self.obstacles:
            if rect.colliderect(obs.rect):
                return True
        return False
    
    def check_portal_collision(self, rect):
        """Check if rect collides with portal"""
        if self.portal and self.portal.active:
            return rect.colliderect(self.portal.rect)
        return False
    
    def next_level(self):
        """Advance to next level"""
        if self.current_level < self.max_levels:
            self.start_level(self.current_level + 1)
            return True
        return False
    
    def is_final_level(self):
        """Check if current level is the last one"""
        return self.current_level >= self.max_levels
    
    def update(self):
        """Update animations"""
        if self.portal:
            self.portal.update()
    
    def draw(self, surface):
        """Draw all obstacles and portal"""
        for obs in self.obstacles:
            obs.draw(surface)
        
        if self.portal:
            self.portal.draw(surface)
