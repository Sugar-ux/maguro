# Import the pygame module
import pygame
from pygame.locals import *
import random
import sys

# Constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize pygame and create the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simplified Game with Stages")

# Define fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('player.png')  # Replace this with your own player image
        self.surf = pygame.transform.scale(self.surf, (120, 60))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT))
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Display home screen
def show_home_screen():
    screen.fill((135, 206, 250))
    title_text = title_font.render("Welcome to the Game!", True, (0, 0, 0))
    start_text = font.render("START (ENTER) ", True, (0, 255, 0))
    quit_text = font.render("EXIT (Quit) ", True, (255, 0, 0))

    screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, SCREEN_HEIGHT / 2 - 80))
    screen.blit(start_text, (SCREEN_WIDTH / 2 - start_text.get_width() / 2, SCREEN_HEIGHT / 2))
    screen.blit(quit_text, (SCREEN_WIDTH / 2 - quit_text.get_width() / 2, SCREEN_HEIGHT / 2 + 40))
    pygame.display.flip()

# Display stage selection screen
def show_stage_selection_screen():
    screen.fill((173, 216, 230))
    title_text = title_font.render("Select Stage", True, (0, 0, 0))
    beginner_text = font.render("1: Beginner (500)", True, (0, 255, 0))
    intermediate_text = font.render("2: Intermediate (1000)", True, (255, 255, 0))
    advanced_text = font.render("3: Advanced (2000)", True, (255, 0, 0))

    screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, SCREEN_HEIGHT / 2 - 120))
    screen.blit(beginner_text, (SCREEN_WIDTH / 2 - beginner_text.get_width() / 2, SCREEN_HEIGHT / 2 - 60))
    screen.blit(intermediate_text, (SCREEN_WIDTH / 2 - intermediate_text.get_width() / 2, SCREEN_HEIGHT / 2))
    screen.blit(advanced_text, (SCREEN_WIDTH / 2 - advanced_text.get_width() / 2, SCREEN_HEIGHT / 2 + 60))
    pygame.display.flip()

# Run game with a target score
def run_game(target_score):
    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)

    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        score += 1
        screen.fill((135, 206, 250))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            show_game_over_screen()
            return

        if score >= target_score:
            show_clear_screen()
            return

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        pygame.display.flip()
        clock.tick(30)

# Display game over screen
def show_game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

# Display game clear screen
def show_clear_screen():
    screen.fill((0, 255, 0))
    clear_text = title_font.render("STAGE CLEAR!", True, (255, 255, 255))
    screen.blit(clear_text, (SCREEN_WIDTH / 2 - clear_text.get_width() / 2, SCREEN_HEIGHT / 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main loop
while True:
    show_home_screen()
    in_home_screen = True

    while in_home_screen:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    in_home_screen = False
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

    show_stage_selection_screen()
    in_stage_selection = True

    while in_stage_selection:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    run_game(500)
                    in_stage_selection = False
                elif event.key == K_2:
                    run_game(1000)
                    in_stage_selection = False
                elif event.key == K_3:
                    run_game(2000)
                    in_stage_selection = False
