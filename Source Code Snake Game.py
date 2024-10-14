# Snake Game 

import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.freetype import *
from pygame.rect import Rect
from enum import Enum


GREEN = (34, 139, 34)
WHITE = (255, 255, 255)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("retrogaming.ttf", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):

        super().__init__()

        self.mouse_over = False

        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)

        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb, bg_rgb)

        self.images = [default_image, highlighted_image]
        self.rects = [default_image.get_rect(center=center_position),
                      highlighted_image.get_rect(center=center_position)]
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class GameState(Enum):
    PLAY = -1
    TITLE = 0
    DEV = 1


def on_grid_random():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return x * 10, y * 10


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()

screen = pygame.display.set_mode((600, 600))

title_btn = UIElement(
    center_position=(300, 100),
    font_size=50,
    bg_rgb=GREEN,
    text_rgb=WHITE,
    text="Snake Game",
    action=GameState.TITLE,
)
play_button = UIElement(
    center_position=(300, 350),
    font_size=50,
    bg_rgb=GREEN,
    text_rgb=WHITE,
    text='Play',
    action=GameState.PLAY,
)
dev_btn = UIElement(
    center_position=(500, 550),
    font_size=15,
    bg_rgb=GREEN,
    text_rgb=WHITE,
    text="By Felipe Salles",
    action=GameState.TITLE,
)


def main_button_function():
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(GREEN)
        if play_button.update(pygame.mouse.get_pos(), mouse_up) is not None:
            return

        play_button.draw(screen)
        title_btn.draw(screen)
        dev_btn.draw(screen)
        pygame.display.flip()


main_button_function()

pygame.display.set_caption('Snake Game')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))
apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.SysFont('retrogaming.ttf', 20)
score = 0
game_over = False

while not game_over:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT

    if collision(snake[0], apple_pos):
        apple_pos == on_grid_random()
        snake.append((0, 0))
        score += 1

    # Check if snake collided with boundaries
    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True
        break
    # Check if the snake has hit itself

    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True
            break
    if game_over:
        break

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    screen.fill((0, 0, 0))
    screen.blit(apple, apple_pos)

    for x in range(0, 600, 10):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, 10):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

    score_font = font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (600 - 120, 10)
    screen.blit(score_font, score_rect)

    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()

while True:
    game_over_font = pygame.font.SysFont('retrogaming.ttf', 80)
    game_over_screen = game_over_font.render('GAME OVER', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 // 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
