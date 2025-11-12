# main.py

import math
import os
import random
import sys
import time

import pygame
from snake import Snake
from food import Food
from score import load_high_score, save_high_score, ScoreRenderer
from menu import Menu, MenuState
from scoreboard import ScoreBoard
from game_settings import Difficulty, GameMode
from leaderboard import Leaderboard
from obstacles import LevelManager

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 700  # Extended height for score board
GAME_AREA_HEIGHT = 600  # Height for actual gameplay
SNAKE_SIZE = 20
FOOD_SIZE = 40
SNAKE_SPEED = 20 # Changed to match SNAKE_SIZE for grid alignment
game_over = False
restart_clicked = False
score = 0
game_paused = False
game_state = MenuState.MAIN  # Start at main menu
current_difficulty = Difficulty.LEVEL_3
current_gamemode = GameMode.CLASSIC
records_button_clicked = None  # Track if records submenu back button was clicked

# Campaign mode variables
campaign_level = 1
level_manager = None  # Will be initialized when campaign starts

# Score management (moved to score.py)
scores_folder = "Scores"
high_score = load_high_score(scores_folder)


# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/Lose My Mind (feat. Doja Cat).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Wave animation settings for food
WAVE_AMPLITUDE = 0  # Amplitude of the wave motion
WAVE_FREQUENCY = 0  # Frequency of the wave motion
wave_phase = 0  # Phase of the wave

# Snake body wave animation settings
SNAKE_WAVE_AMPLITUDE = 0  # Amplitude for snake body wave motion
SNAKE_WAVE_FREQUENCY = 0  # Frequency for snake body wave motion
snake_wave_phase = 0  # Initial phase for snake body wave

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")


# Load sprite images
snake_head_sprite = pygame.image.load("assets/snake_head.png")
snake_head_sprite = pygame.transform.scale(snake_head_sprite, (SNAKE_SIZE, SNAKE_SIZE))

food_sprite = pygame.image.load("assets/snake_food.png")
food_sprite = pygame.transform.scale(food_sprite, (FOOD_SIZE, FOOD_SIZE))

snake_body_sprite = pygame.image.load("assets/snake_body.png")
snake_body_sprite = pygame.transform.scale(snake_body_sprite, (SNAKE_SIZE, SNAKE_SIZE))

restart_button_sprite = pygame.image.load("assets/snake_restart_button.png")

background_image = pygame.image.load("assets/Pixel_Art_Forest_Trees_And_Sky_Landscape_high_resolution_preview_3293114.jpg")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Load sound effects
eat_sound = pygame.mixer.Sound("assets/eat_sound.wav")

button_click_sound = pygame.mixer.Sound("assets/button_click_sound.wav")

# Snake setup
snake = Snake([100, 60], SNAKE_SIZE, SNAKE_SPEED, snake_head_sprite, snake_body_sprite)

# Food setup
food = Food(SCREEN_WIDTH, GAME_AREA_HEIGHT, SNAKE_SIZE, FOOD_SIZE, food_sprite)

# Font settings
font_path = "assets/font.ttf"
font_size = 27
font_color = (255, 255, 255)  # White color

# Score renderer (delegated to score.py)
score_renderer = ScoreRenderer(font_path, font_color)

# Menu setup
menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT, font_path, background_image, GAME_AREA_HEIGHT)

# Scoreboard setup (for the stats panel below the game)
scoreboard = ScoreBoard(0, GAME_AREA_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GAME_AREA_HEIGHT, font_path, font_size - 2)

# Leaderboard setup
leaderboard = Leaderboard()


# Particle System
class Particle:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(5, 10)

        # Adjust velocity based on the snake's direction
        velocity = random.uniform(1, 3)
        if direction == "UP":
            self.x_vel = random.uniform(-1, 1)
            self.y_vel = -velocity
        elif direction == "DOWN":
            self.x_vel = random.uniform(-1, 1)
            self.y_vel = velocity
        elif direction == "LEFT":
            self.x_vel = -velocity
            self.y_vel = random.uniform(-1, 1)
        elif direction == "RIGHT":
            self.x_vel = velocity
            self.y_vel = random.uniform(-1, 1)
        else:
            self.x_vel = random.uniform(-1, 1)
            self.y_vel = random.uniform(-1, 1)

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.x, self.y, self.size, self.size])


# New list to hold particles
particles = []


# Game loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle menu clicks
            if game_state in [MenuState.MAIN, MenuState.SUBMENU_PLAY, MenuState.SUBMENU_DIFFICULTY, 
                              MenuState.SUBMENU_GAMEMODE, MenuState.SUBMENU_RECORDS, MenuState.PAUSED, MenuState.GAME_OVER]:
                action = menu.handle_click(mouse_pos, game_state)
                
                if action == 'start_game':
                    # Initialize a new game with current settings
                    score = 0
                    game_over = False
                    game_paused = False
                    snake = Snake([100, 60], SNAKE_SIZE, menu.current_difficulty.value, snake_head_sprite, snake_body_sprite)
                    food = Food(SCREEN_WIDTH, GAME_AREA_HEIGHT, SNAKE_SIZE, FOOD_SIZE, food_sprite)
                    particles = []
                    wave_phase = 0
                    current_difficulty = menu.current_difficulty
                    current_gamemode = menu.current_gamemode
                    
                    # Initialize campaign mode if selected
                    if current_gamemode == GameMode.CAMPAIGN:
                        campaign_level = 1
                        level_manager = LevelManager(SCREEN_WIDTH, GAME_AREA_HEIGHT, SNAKE_SIZE)
                        level_manager.start_level(campaign_level)
                    else:
                        level_manager = None
                    
                    pygame.mixer.music.play(-1)
                    game_state = MenuState.PLAYING
                    button_click_sound.play()
                
                elif action == 'open_play_menu':
                    game_state = MenuState.SUBMENU_PLAY
                    button_click_sound.play()
                elif action == 'open_difficulty_menu':
                    game_state = MenuState.SUBMENU_DIFFICULTY
                    button_click_sound.play()
                elif action == 'open_gamemode_menu':
                    game_state = MenuState.SUBMENU_GAMEMODE
                    button_click_sound.play()
                elif action == 'open_records_menu':
                    game_state = MenuState.SUBMENU_RECORDS
                    records_button_clicked = None
                    button_click_sound.play()
                
                elif action == 'difficulty_selected':
                    button_click_sound.play()
                elif action == 'gamemode_selected':
                    button_click_sound.play()
                
                elif action == 'back_to_play':
                    game_state = MenuState.SUBMENU_PLAY
                    button_click_sound.play()
                elif action == 'back_to_main':
                    game_state = MenuState.MAIN
                    pygame.mixer.music.stop()
                    button_click_sound.play()
                
                elif action == 'resume':
                    game_paused = False
                    game_state = MenuState.PLAYING
                    pygame.mixer.music.unpause()
                    button_click_sound.play()
                elif action == 'restart':
                    score = 0
                    game_over = False
                    game_paused = False
                    snake = Snake([100, 60], SNAKE_SIZE, menu.current_difficulty.value, snake_head_sprite, snake_body_sprite)
                    food = Food(SCREEN_WIDTH, GAME_AREA_HEIGHT, SNAKE_SIZE, FOOD_SIZE, food_sprite)
                    particles = []
                    wave_phase = 0
                    pygame.mixer.music.play(-1)
                    game_state = MenuState.PLAYING
                    button_click_sound.play()
                
                elif action == 'quit':
                    pygame.quit()
                    sys.exit()
            
            # Handle records submenu back button click
            if game_state == MenuState.SUBMENU_RECORDS:
                back_btn = menu.draw_records_submenu(screen, leaderboard)
                if back_btn.is_clicked(mouse_pos):
                    game_state = MenuState.SUBMENU_PLAY
                    button_click_sound.play()
        
        elif event.type == pygame.KEYDOWN:
            # Pause/Resume with ESC key
            if event.key == pygame.K_ESCAPE and game_state == MenuState.PLAYING:
                game_paused = True
                game_state = MenuState.PAUSED
                pygame.mixer.music.pause()
            elif game_state == MenuState.PLAYING:
                # Snake direction controls only during gameplay
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.change_to = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.change_to = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.change_to = "RIGHT"

    # Update menu hover states
    if game_state in [MenuState.MAIN, MenuState.SUBMENU_PLAY, MenuState.SUBMENU_DIFFICULTY, 
                      MenuState.SUBMENU_GAMEMODE, MenuState.PAUSED, MenuState.GAME_OVER]:
        menu.update(mouse_pos, game_state)

    # Game logic only runs during gameplay
    if game_state == MenuState.PLAYING and not game_over:
        # Update the direction and move the snake
        snake.update_direction()
        snake.move()

        # Check collision with food - AABB
        if (
            snake.pos[0] < food.pos[0] + FOOD_SIZE
            and snake.pos[0] + SNAKE_SIZE > food.pos[0]
            and snake.pos[1] < food.pos[1] + FOOD_SIZE
            and snake.pos[1] + SNAKE_SIZE > food.pos[1]
        ):
            score += 1
            # Update high score if current score exceeds it
            if score > high_score:
                high_score = score
            food.spawn = False
            
            # Campaign mode: track food eaten
            if current_gamemode == GameMode.CAMPAIGN and level_manager:
                level_manager.on_food_eaten()
            
            for _ in range(20):  # Create 20 particles
                color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
                particles.append(Particle(snake.pos[0], snake.pos[1], color, snake.direction))
            print("Food eaten at", food.pos)  # Debug message
        else:
            snake.shrink_tail()

        # Update wave phase
        wave_phase += WAVE_FREQUENCY

        # Update snake wave phase
        snake_wave_phase += SNAKE_WAVE_FREQUENCY

        # Food spawn
        if not food.spawn:
            # In campaign mode, avoid spawning food on obstacles
            if current_gamemode == GameMode.CAMPAIGN and level_manager:
                attempts = 0
                while attempts < 100:
                    food.respawn(snake.body)
                    food_rect = pygame.Rect(food.pos[0], food.pos[1], FOOD_SIZE, FOOD_SIZE)
                    if not level_manager.check_obstacle_collision(food_rect):
                        break
                    attempts += 1
            else:
                food.respawn(snake.body)
            print("New food position:", food.pos)  # Debug message
            eat_sound.play()

        # Collision detection based on game mode
        # CLASSIC: Can go through walls, only dies on body collision
        # MODERN: Dies on wall collision and body collision
        # CAMPAIGN: Can go through walls, dies on obstacle and body collision
        
        if current_gamemode == GameMode.CLASSIC:
            # Wrap around walls (teleport to other side)
            wrapped = False
            if snake.pos[0] < 0:
                snake.pos[0] = SCREEN_WIDTH - SNAKE_SIZE
                wrapped = True
            elif snake.pos[0] >= SCREEN_WIDTH:
                snake.pos[0] = 0
                wrapped = True
            if snake.pos[1] < 0:
                snake.pos[1] = GAME_AREA_HEIGHT - SNAKE_SIZE
                wrapped = True
            elif snake.pos[1] >= GAME_AREA_HEIGHT:
                snake.pos[1] = 0
                wrapped = True
            
            # If wrapped, update body to follow head immediately
            if wrapped and len(snake.body) > 0:
                snake.body[0] = snake.pos[:]
            
            # Only check self collision
            if snake.check_self_collision():
                game_over = True
                leaderboard.add_score(score, current_difficulty, current_gamemode)
        
        elif current_gamemode == GameMode.MODERN:
            # Check wall collision
            if snake.check_wall_collision(SCREEN_WIDTH, GAME_AREA_HEIGHT):
                game_over = True
                leaderboard.add_score(score, current_difficulty, current_gamemode)
            # Check self collision
            if snake.check_self_collision():
                game_over = True
                leaderboard.add_score(score, current_difficulty, current_gamemode)
        
        elif current_gamemode == GameMode.CAMPAIGN:
            # Wrap around walls (like CLASSIC)
            wrapped = False
            if snake.pos[0] < 0:
                snake.pos[0] = SCREEN_WIDTH - SNAKE_SIZE
                wrapped = True
            elif snake.pos[0] >= SCREEN_WIDTH:
                snake.pos[0] = 0
                wrapped = True
            if snake.pos[1] < 0:
                snake.pos[1] = GAME_AREA_HEIGHT - SNAKE_SIZE
                wrapped = True
            elif snake.pos[1] >= GAME_AREA_HEIGHT:
                snake.pos[1] = 0
                wrapped = True
            
            # If wrapped, update body to follow head immediately
            if wrapped and len(snake.body) > 0:
                snake.body[0] = snake.pos[:]
            
            # Check obstacle collision
            if level_manager:
                snake_rect = pygame.Rect(snake.pos[0], snake.pos[1], SNAKE_SIZE, SNAKE_SIZE)
                if level_manager.check_obstacle_collision(snake_rect):
                    game_over = True
                    leaderboard.add_score(score, current_difficulty, current_gamemode)
                
                # Check portal collision (advance to next level)
                if level_manager.check_portal_collision(snake_rect):
                    if level_manager.is_final_level():
                        # Won the campaign!
                        game_over = True
                        leaderboard.add_score(score, current_difficulty, current_gamemode)
                    else:
                        # Advance to next level
                        level_manager.next_level()
                        # Reset snake position
                        snake.pos = [100, 60]
                        snake.body = [snake.pos[:]]
                        snake.direction = "RIGHT"
                        snake.change_to = "RIGHT"
            
            # Check self collision
            if snake.check_self_collision():
                game_over = True
                leaderboard.add_score(score, current_difficulty, current_gamemode)

        # If game over, transition to game over menu
        if game_over:
            pygame.mixer.music.stop()
            save_high_score(scores_folder, high_score)
            game_state = MenuState.GAME_OVER

    # Rendering
    screen.blit(background_image, (0, 0))

    # Draw gameplay elements only if not in menu
    if game_state == MenuState.PLAYING:
        # Draw obstacles and portal in campaign mode
        if current_gamemode == GameMode.CAMPAIGN and level_manager:
            level_manager.update()
            level_manager.draw(screen)
        
        # Draw snake (body + head)
        snake.draw(screen)

        # Draw food
        food.draw(screen, wave_phase, WAVE_AMPLITUDE)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

    # Draw menu based on game state
    if game_state == MenuState.MAIN:
        menu.draw_main_menu(screen)
    elif game_state == MenuState.SUBMENU_PLAY:
        menu.draw_play_submenu(screen)
    elif game_state == MenuState.SUBMENU_DIFFICULTY:
        menu.draw_difficulty_submenu(screen)
    elif game_state == MenuState.SUBMENU_GAMEMODE:
        menu.draw_gamemode_submenu(screen)
    elif game_state == MenuState.SUBMENU_RECORDS:
        menu.draw_records_submenu(screen, leaderboard)
    elif game_state == MenuState.PAUSED:
        menu.draw_pause_menu(screen)
    elif game_state == MenuState.GAME_OVER:
        menu.draw_gameover_menu(screen, score)
    
    # Draw scoreboard at the bottom (only during gameplay)
    if game_state == MenuState.PLAYING:
        if current_gamemode == GameMode.CAMPAIGN and level_manager:
            scoreboard.draw(screen, score, level_manager)
        else:
            scoreboard.draw(screen, score)

    # Refresh game screen
    pygame.display.update()
    pygame.time.Clock().tick(20)
