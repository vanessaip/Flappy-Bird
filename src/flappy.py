import pygame
import sys
import random

# Window constants
SCREEN_HEIGHT = 700     # changing SCREEN_HEIGHT scales the rest of the graphics as well
SCALE = SCREEN_HEIGHT / 512     # original background image height
SCREEN_WIDTH = round(288 * SCALE)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_font = pygame.font.Font('04B_19.ttf', round(37 * SCALE))
game_font2 = pygame.font.Font('04B_19.ttf', round(40 * SCALE))


# draws 2 floor images beside each other starting at floor_x
def draw_floor(floor_x):
    screen.blit(floor, (floor_x, FLOOR_Y))
    screen.blit(floor, (floor_x + floor.get_width(), FLOOR_Y))


# draws bird at bird_rect
def draw_bird(bird_index, bird_rect, movement):
    angle = -movement * 4.5
    if angle < -90:
        angle = -90
    img = pygame.transform.rotozoom(bird[bird_index], angle, 1)
    screen.blit(img, bird_rect)


# draws pipes at pipe_rects at correct orientation
def draw_pipes(pipe_rects):
    for p in pipe_rects:
        if p.bottom >= FLOOR_Y:                 # if pipe is facing up
            screen.blit(pipe, p)     # pipe is a rect (coordinates)
        else:
            screen.blit(pygame.transform.flip(pipe, False, True), p)


# draws score
def draw_score():
    text = game_font.render(str(score), True, (255, 255, 255))
    shadow = game_font2.render(str(score), True, (0, 0, 0))

    screen.blit(shadow, (SCREEN_WIDTH / 2 + 1, SCREEN_HEIGHT / 6))
    screen.blit(text, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))


# returns rects for new pair of pipes   !!! make resizable
def load_pipe_rects():
    x_pos = SCREEN_WIDTH + 100
    y_pos = random.choice(PIPE_HEIGHTS)
    bottom = pipe.get_rect(midtop=(x_pos, y_pos))
    top = pipe.get_rect(midbottom=(x_pos, y_pos - 109 * SCALE))
    return bottom, top


# shifts pipe rects x left by 5 and returns pipes visible on screen
def move_pipes(pipe_rects):
    for p in pipe_rects:
        p.centerx -= SCROLL_SPEED
    visible_pipes = [p for p in pipe_rects if p.right > -50]
    return visible_pipes


# returns true if bird_rect does not collide with any of the pipe_rects, otherwise returns false
def check_collision(bird_rect, pipe_rects):
    if bird_rect.collidelist(pipe_rects) != -1 or (bird_rect.top <= 0 and collide_pipe_left(bird_rect, pipe_rects)):
        collide_sound.play()
        return False
    return True


# returns true if rect collides with any rect in rect_list, otherwise returns false
def collide_pipe_left(rect, rect_list):
    for r in rect_list:
        if rect.right >= r.left:
            return True
        return False


# increments score if the centerx of one of pipe_rects is within 2 pixels of BIRD_X, otherwise does nothing
def check_score(pipe_rects):
    global score

    for p in pipe_rects[::2]:       # every other in pipe_rects
        if BIRD_X - 2 < p.centerx < BIRD_X + 2:
            score += 1
            score_sound.play()


# returns scaled image with filename
def load_image(filename):
    img = pygame.image.load('assets/' + filename + '.png').convert_alpha()
    return pygame.transform.scale(img, (round(img.get_width() * SCALE), round(img.get_height() * SCALE)))


# Images
bg = load_image('background-day')
floor = load_image('base')
bird_colour = random.choice(['red', 'blue', 'yellow'])
bird = [load_image(bird_colour + 'bird-upflap'), load_image(bird_colour + 'bird-midflap'),
        load_image(bird_colour + 'bird-downflap')]
pipe = load_image('pipe-green')

# Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collide_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# Rendering constants
BIRD_X = SCREEN_WIDTH / 3
BIRD_START_Y = SCREEN_HEIGHT / 3

PIPE_HEIGHTS = [height * SCALE for height in [365, 328, 255, 182]]

FLOOR_Y = SCREEN_HEIGHT - floor.get_height()

SCROLL_SPEED = 3

# Bird variables
bird_index = 0
bird_rect = bird[bird_index].get_rect(center=(BIRD_X, BIRD_START_Y))        # used to manipulate bird position
GRAVITY = 0.7       # TODO: make resizable 0.7, 9
JUMP = 9
movement = 0
FLAP = pygame.event.custom_type()
pygame.time.set_timer(FLAP, 50)

# Pipe variables
pipe_rects = []
SPAWN_PIPE = pygame.event.custom_type()
pygame.time.set_timer(SPAWN_PIPE, 1300)     # TODO: resizable original: 1200

# Floor x pos
floor_x = 0

# Score
score = 0

# Game state
playing = True


def draw():
    screen.blit(bg, (0, 0))
    draw_pipes(pipe_rects)
    draw_floor(floor_x)
    draw_bird(bird_index, bird_rect, movement)
    draw_score()

# TODO: multiple hit sounds/continuing even after collision if space bar is pressed
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if playing:
            if event.type == pygame.KEYDOWN:        # could just make any key the command
                if event.key == pygame.K_SPACE:
                    movement = -JUMP
                    flap_sound.play()

            if event.type == FLAP:
                bird_index = (bird_index + 1) % 3       # 3 frames

            if event.type == SPAWN_PIPE:
                pipe_rects.extend(load_pipe_rects())
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = True
                    bird_rect.centery = BIRD_START_Y
                    movement = 0
                    pipe_rects.clear()
                    score = 0
# Continuous stuff
    if bird_rect.bottom < FLOOR_Y - 15:
        # update bird rect
        movement += GRAVITY
        bird_rect.centery += movement
    else:
        playing = False

    if playing:
        # check collision
        playing = check_collision(bird_rect, pipe_rects)

        # update score
        check_score(pipe_rects)

        # scroll pipes
        pipe_rects = move_pipes(pipe_rects)

        # scroll floor
        floor_x -= SCROLL_SPEED
        if floor_x <= -floor.get_width():
            floor_x = 0
    else:        # pause the scrolling and let the bird hit the ground if it hasn't already
        pass

    draw()
    pygame.display.update()
    pygame.time.Clock().tick(60)
