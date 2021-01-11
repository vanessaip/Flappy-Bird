import pygame
import sys
import random

# Rendering constants
SCREEN_HEIGHT = 700
SCALE = SCREEN_HEIGHT / 512
SCREEN_WIDTH = round(288 * SCALE)

BIRD_X = SCREEN_WIDTH / 3
BIRD_START_Y = SCREEN_HEIGHT / 2

# FLOOR_Y = SCREEN_HEIGHT - floor.get_height()

GRAVITY = 0.7
JUMP = 9

BIRD_COLOURS = ['red', 'blue', 'yellow']
PIPE_HEIGHTS = [500, 450, 350, 250]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_font = pygame.font.Font('04B_19.ttf', 40)


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


# returns rects for new pair of pipes
def load_pipe_rects():
    x_pos = SCREEN_WIDTH + 100
    y_pos = random.choice(PIPE_HEIGHTS)
    bottom = pipe.get_rect(midtop=(x_pos, y_pos))
    top = pipe.get_rect(midbottom=(x_pos, y_pos - 150))
    return bottom, top


# shifts pipe rects x left by 5 and returns pipes visible on screen
def move_pipes():
    for p in pipe_rects:
        p.centerx -= 2
    visible_pipes = [pipe for pipe in pipe_rects if pipe.right > -50]
    return visible_pipes

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

floor_x = 0

pipe_rects = []
SPAWN_PIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE, 2000)

bird_index = 0
bird_rect = bird[bird_index].get_rect(center=(BIRD_X, BIRD_START_Y))
movement = 0
FLAP = pygame.USEREVENT
pygame.time.set_timer(FLAP, 50)


def draw():
    screen.blit(bg, (0, 0))
    draw_bird()
    draw_pipes()
    draw_floor()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                movement = -JUMP

        if event.type == FLAP:
            bird_index = (bird_index + 1) % 3       # 3 frames

        if event.type == SPAWN_PIPE:
            pipe_rects.extend(load_pipe_rects())

    # update bird rect
    movement += GRAVITY

    # scroll pipes
    pipe_rects = move_pipes()

    # scroll floor
    floor_x -= 2
    if floor_x <= -floor.get_width():
        floor_x = 0

    draw()
    pygame.display.update()
    pygame.time.Clock().tick(60)
