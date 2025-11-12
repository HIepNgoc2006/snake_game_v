import pygame


class ScoreBoard:
    def __init__(self, x, y, width, height, font_path, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font_path, font_size)
        self.font_large = pygame.font.Font(font_path, font_size + 4)
        self.font_small = pygame.font.Font(font_path, font_size - 6)
        self.bg_color = (20, 20, 20)
        self.border_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.highlight_color = (0, 255, 0)
        self.campaign_color = (255, 215, 0)  # Gold for campaign info

    def draw(self, surface, score, level_manager=None):
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        if level_manager:
            # Campaign mode - show score, level, and food count
            y_offset = self.rect.y + 15
            
            # Score
            score_text = f"Score: {score}"
            score_surface = self.font_large.render(score_text, True, self.highlight_color)
            score_rect = score_surface.get_rect(center=(self.rect.centerx, y_offset))
            surface.blit(score_surface, score_rect)
            
            # Level info
            y_offset += 35
            level_text = f"Level: {level_manager.current_level}/{level_manager.max_levels}"
            level_surface = self.font.render(level_text, True, self.campaign_color)
            level_rect = level_surface.get_rect(center=(self.rect.centerx, y_offset))
            surface.blit(level_surface, level_rect)
            
            # Food count
            y_offset += 28
            food_text = f"Food: {level_manager.food_eaten_this_level}/{level_manager.food_required_for_portal}"
            food_surface = self.font_small.render(food_text, True, self.text_color)
            food_rect = food_surface.get_rect(center=(self.rect.centerx, y_offset))
            surface.blit(food_surface, food_rect)
        else:
            # Normal mode - just show score centered
            score_text = f"Score: {score}"
            score_surface = self.font_large.render(score_text, True, self.highlight_color)
            score_rect = score_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(score_surface, score_rect)
        
