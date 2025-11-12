import pygame
from enum import Enum
from game_settings import Difficulty, GameMode, DIFFICULTY_NAMES, GAMEMODE_DESCRIPTIONS


class MenuState(Enum):
    MAIN = 1
    SUBMENU_PLAY = 2
    SUBMENU_DIFFICULTY = 3
    SUBMENU_GAMEMODE = 4
    SUBMENU_RECORDS = 5
    PAUSED = 6
    GAME_OVER = 7
    PLAYING = 8


class Button:
    def __init__(self, x, y, width, height, text, font, font_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.bg_color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Menu:
    def __init__(self, screen_width, screen_height, font_path, background_image, game_area_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_area_height = game_area_height
        self.background_image = background_image
        self.font = pygame.font.Font(font_path, 36)
        self.small_font = pygame.font.Font(font_path, 18)
        self.tiny_font = pygame.font.Font(font_path, 14)
        self.state = MenuState.MAIN
        self.current_difficulty = Difficulty.LEVEL_3
        self.current_gamemode = GameMode.CLASSIC

        # Main menu buttons
        button_width, button_height = 200, 50
        start_x = (screen_width - button_width) // 2
        self.main_play_button = Button(start_x, game_area_height // 2 - 60, button_width, button_height, "PLAY", self.font)
        self.main_quit_button = Button(start_x, game_area_height // 2 + 20, button_width, button_height, "QUIT", self.font)

        # PLAY submenu buttons
        play_w, play_h = 180, 40
        play_x = (screen_width - play_w) // 2
        self.play_new_game_button = Button(play_x, 150, play_w, play_h, "NEW GAME", self.small_font)
        self.play_difficulty_button = Button(play_x, 210, play_w, play_h, "DIFFICULTY", self.small_font)
        self.play_gamemode_button = Button(play_x, 270, play_w, play_h, "GAME MODE", self.small_font)
        self.play_records_button = Button(play_x, 330, play_w, play_h, "RECORDS", self.small_font)
        self.play_back_button = Button(play_x, 390, 120, 36, "BACK", self.small_font)

        # Difficulty buttons
        diff_w, diff_h = 140, 32
        diff_x = (screen_width - diff_w) // 2
        self.difficulty_buttons = []
        for i, diff in enumerate(Difficulty):
            y = 100 + i * 45
            self.difficulty_buttons.append(Button(diff_x, y, diff_w, diff_h, DIFFICULTY_NAMES[diff], self.small_font))
        self.difficulty_back_button = Button(diff_x, game_area_height - 80, 120, 36, "BACK", self.small_font)

        # Gamemode buttons
        gm_w, gm_h = 200, 40
        gm_x = (screen_width - gm_w) // 2
        self.gamemode_buttons = [
            (GameMode.CLASSIC, Button(gm_x, 150, gm_w, gm_h, "CLASSIC", self.small_font)),
            (GameMode.MODERN, Button(gm_x, 210, gm_w, gm_h, "MODERN", self.small_font)),
            (GameMode.CAMPAIGN, Button(gm_x, 270, gm_w, gm_h, "CAMPAIGN", self.small_font)),
        ]
        self.gamemode_back_button = Button(gm_x, game_area_height - 80, 120, 36, "BACK", self.small_font)

        # Pause/menu buttons
        p_w, p_h = 160, 48
        p_x = (screen_width - p_w) // 2
        self.pause_resume_button = Button(p_x, game_area_height // 2 - 60, p_w, p_h, "RESUME", self.font)
        self.pause_menu_button = Button(p_x, game_area_height // 2 + 10, p_w, p_h, "MENU", self.font)

        # Game over buttons
        go_w, go_h = 160, 40
        go_x = (screen_width - go_w) // 2
        self.gameover_restart_button = Button(go_x, game_area_height // 2 + 20, go_w, go_h, "RESTART", self.small_font)
        self.gameover_menu_button = Button(go_x, game_area_height // 2 + 80, go_w, go_h, "MENU", self.small_font)

    # Draw methods
    def draw_main_menu(self, surface):
        surface.blit(self.background_image, (0, 0))
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("SNAKE GAME", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(title_surface, title_rect)
        self.main_play_button.draw(surface)
        self.main_quit_button.draw(surface)

    def draw_play_submenu(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("PLAY", True, (0, 255, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(title_surface, title_rect)
        self.play_new_game_button.draw(surface)
        self.play_difficulty_button.draw(surface)
        self.play_gamemode_button.draw(surface)
        self.play_records_button.draw(surface)
        self.play_back_button.draw(surface)

    def draw_difficulty_submenu(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("SELECT DIFFICULTY", True, (255, 200, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_surface, title_rect)
        for i, btn in enumerate(self.difficulty_buttons):
            btn.is_hovered = False
            btn.draw(surface)
        self.difficulty_back_button.draw(surface)

    def draw_gamemode_submenu(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("SELECT GAME MODE", True, (0, 200, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_surface, title_rect)
        for mode, btn in self.gamemode_buttons:
            btn.draw(surface)
            desc = GAMEMODE_DESCRIPTIONS.get(mode, "")
            desc_surface = self.tiny_font.render(desc, True, (200, 200, 200))
            desc_rect = desc_surface.get_rect(center=(self.screen_width // 2, btn.rect.bottom + 12))
            surface.blit(desc_surface, desc_rect)
        self.gamemode_back_button.draw(surface)

    def draw_records_submenu(self, surface, leaderboard):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("TOP 10 RECORDS", True, (255, 215, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 30))
        surface.blit(title_surface, title_rect)
        scores = leaderboard.get_top_scores()
        y_pos = 80
        for rank, entry in enumerate(scores, 1):
            rank_text = f"{rank}. Score: {entry['score']} - {entry['difficulty']} - {entry['date']}"
            score_surface = self.tiny_font.render(rank_text, True, (255, 255, 255))
            surface.blit(score_surface, (20, y_pos))
            y_pos += 25
        if not scores:
            empty_text = self.small_font.render("No records yet!", True, (200, 100, 100))
            empty_rect = empty_text.get_rect(center=(self.screen_width // 2, 200))
            surface.blit(empty_text, empty_rect)
        back_button = Button(self.screen_width // 2 - 50, self.screen_height - 80, 100, 40, "BACK", self.small_font)
        back_button.draw(surface)
        return back_button

    def draw_pause_menu(self, surface):
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(title_surface, title_rect)
        self.pause_resume_button.draw(surface)
        self.pause_menu_button.draw(surface)

    def draw_gameover_menu(self, surface, score, high_score=None):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title_surface = self.font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(title_surface, title_rect)
        score_text = self.small_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 160))
        surface.blit(score_text, score_rect)
        self.gameover_restart_button.draw(surface)
        self.gameover_menu_button.draw(surface)

    # Input handling
    def update(self, mouse_pos, state):
        self.state = state
        if state == MenuState.MAIN:
            self.main_play_button.update(mouse_pos)
            self.main_quit_button.update(mouse_pos)
        elif state == MenuState.SUBMENU_PLAY:
            self.play_new_game_button.update(mouse_pos)
            self.play_difficulty_button.update(mouse_pos)
            self.play_gamemode_button.update(mouse_pos)
            self.play_records_button.update(mouse_pos)
            self.play_back_button.update(mouse_pos)
        elif state == MenuState.SUBMENU_DIFFICULTY:
            for btn in self.difficulty_buttons:
                btn.update(mouse_pos)
            self.difficulty_back_button.update(mouse_pos)
        elif state == MenuState.SUBMENU_GAMEMODE:
            for _, btn in self.gamemode_buttons:
                btn.update(mouse_pos)
            self.gamemode_back_button.update(mouse_pos)
        elif state == MenuState.SUBMENU_RECORDS:
            # back button produced by draw_records_submenu; we won't track hover here
            pass
        elif state == MenuState.PAUSED:
            self.pause_resume_button.update(mouse_pos)
            self.pause_menu_button.update(mouse_pos)
        elif state == MenuState.GAME_OVER:
            self.gameover_restart_button.update(mouse_pos)
            self.gameover_menu_button.update(mouse_pos)

    def handle_click(self, mouse_pos, state):
        # MAIN
        if state == MenuState.MAIN:
            if self.main_play_button.is_clicked(mouse_pos):
                return 'open_play_menu'
            if self.main_quit_button.is_clicked(mouse_pos):
                return 'quit'

        # PLAY submenu
        if state == MenuState.SUBMENU_PLAY:
            if self.play_new_game_button.is_clicked(mouse_pos):
                return 'start_game'
            if self.play_difficulty_button.is_clicked(mouse_pos):
                return 'open_difficulty_menu'
            if self.play_gamemode_button.is_clicked(mouse_pos):
                return 'open_gamemode_menu'
            if self.play_records_button.is_clicked(mouse_pos):
                return 'open_records_menu'
            if self.play_back_button.is_clicked(mouse_pos):
                return 'back_to_main'

        # DIFFICULTY
        if state == MenuState.SUBMENU_DIFFICULTY:
            for i, btn in enumerate(self.difficulty_buttons):
                if btn.is_clicked(mouse_pos):
                    # set selected difficulty
                    self.current_difficulty = list(Difficulty)[i]
                    return 'difficulty_selected'
            if self.difficulty_back_button.is_clicked(mouse_pos):
                return 'back_to_play'

        # GAMEMODE
        if state == MenuState.SUBMENU_GAMEMODE:
            for mode, btn in self.gamemode_buttons:
                if btn.is_clicked(mouse_pos):
                    self.current_gamemode = mode
                    return 'gamemode_selected'
            if self.gamemode_back_button.is_clicked(mouse_pos):
                return 'back_to_play'

        # RECORDS
        if state == MenuState.SUBMENU_RECORDS:
            # The back button is drawn by draw_records_submenu and returned to the caller for click testing.
            # We still handle it defensively here if needed.
            # No direct clickable elements here otherwise.
            return None

        # PAUSED
        if state == MenuState.PAUSED:
            if self.pause_resume_button.is_clicked(mouse_pos):
                return 'resume'
            if self.pause_menu_button.is_clicked(mouse_pos):
                return 'back_to_main'

        # GAME OVER
        if state == MenuState.GAME_OVER:
            if self.gameover_restart_button.is_clicked(mouse_pos):
                return 'restart'
            if self.gameover_menu_button.is_clicked(mouse_pos):
                return 'back_to_main'

        return None
