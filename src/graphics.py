import pygame
import random

# Rendering constants
SCREEN_HEIGHT = 700
SCALE = SCREEN_HEIGHT / 512
SCREEN_WIDTH = round(288 * SCALE)

BIRD_X = SCREEN_WIDTH / 3
BIRD_START_Y = SCREEN_HEIGHT / 2

# FLOOR_Y = SCREEN_HEIGHT - floor.get_height()

BIRD_COLOURS = ['red', 'blue', 'yellow']
PIPE_HEIGHTS = [500, 450, 350, 250]


# places 2 floor images beside each other starting at floor_x
def draw_floor():
    y_pos = SCREEN_HEIGHT - floor.get_height()
    screen.blit(floor, (floor_x, y_pos))
    screen.blit(floor, (floor_x + floor.get_width(), y_pos))


# draws bird at updated y position
def draw_bird():
    bird_rect.centery += movement
    img = pygame.transform.rotozoom(bird[bird_index], -movement * 4, 1)
    screen.blit(img, bird_rect)


def draw_pipes():
    for p in pipe_rects:
        if p.bottom >= SCREEN_HEIGHT - floor.get_height():                 # if pipe is facing up
            screen.blit(pipe, p)     # pipe is a rect (coordinates)
        else:
            screen.blit(pygame.transform.flip(pipe, False, True), p)


# Images
def load_image(filename):
    img = pygame.image.load('assets/' + filename + '.png').convert_alpha()
    return pygame.transform.scale(img, (round(img.get_width() * SCALE), round(img.get_height() * SCALE)))


bg = load_image('background-day')
floor = load_image('base')
bird_colour = random.choice(BIRD_COLOURS)
bird = [load_image(bird_colour + 'bird-upflap'), load_image(bird_colour + 'bird-midflap'),
        load_image(bird_colour + 'bird-downflap')]
pipe = load_image('pipe-green')