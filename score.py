import os
import math
import time
import pygame


def load_high_score(scores_folder="Scores", filename="high_score.txt"):
    # Ensure folder exists
    if not os.path.exists(scores_folder):
        os.makedirs(scores_folder)
    path = os.path.join(scores_folder, filename)
    high_score = 0
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                high_score = int(f.read().strip())
        except (ValueError, FileNotFoundError):
            high_score = 0
    return high_score


def save_high_score(scores_folder, high_score, filename="high_score.txt"):
    if not os.path.exists(scores_folder):
        os.makedirs(scores_folder)
    path = os.path.join(scores_folder, filename)
    with open(path, "w") as f:
        f.write(str(high_score))


class ScoreRenderer:
    def __init__(self, font_path, font_color=(255, 255, 255)):
        self.font_path = font_path
        self.font_color = font_color

    def draw(self, surface, text, size, x, y, outline_thickness=2, wave_amplitude=5, wave_frequency=2):
        font = pygame.font.Font(self.font_path, size)
        outline_color = (0, 0, 0)

        def render_with_outline(message, font, main_color, outline_color, thickness):
            base = font.render(message, True, main_color)
            outline_size = (base.get_width() + 2 * thickness, base.get_height() + 2 * thickness)
            outline = pygame.Surface(outline_size, pygame.SRCALPHA)
            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx != 0 or dy != 0:
                        temp = font.render(message, True, outline_color)
                        outline.blit(temp, (dx + thickness, dy + thickness))
            outline.blit(base, (thickness, thickness))
            return outline

        # Time-based wave phase
        time_ms = time.time() * 1000
        phase = wave_frequency * time_ms / 1000
        wave_offset = wave_amplitude * math.sin(phase)
        y_with_wave = y + wave_offset

        text_surface = render_with_outline(text, font, self.font_color, outline_color, outline_thickness)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y_with_wave)
        surface.blit(text_surface, text_rect)
