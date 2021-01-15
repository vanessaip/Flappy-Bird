import pygame
import sys
import random

# Window constants
SCREEN_HEIGHT = 700     # changing SCREEN_HEIGHT scales the rest of the graphics as well // TODO: <= 500 cuts off bird
SCALE = SCREEN_HEIGHT / 512     # original background image height
SCREEN_WIDTH = round(288 * SCALE)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_font = pygame.font.Font('04B_19.ttf', round(28 * SCALE))       # 37, 40
game_font2 = pygame.font.Font('04B_19.ttf', round(29 * SCALE))


# draws 2 floor images beside each other starting at floor_x
def draw_floor(floor_x):
    screen.blit(floor, (floor_x, FLOOR_Y))
    screen.blit(floor, (floor_x + floor.get_width(), FLOOR_Y))


# draws bird at bird_rect
def draw_bird(bird_index, bird_rect, movement):
    angle = -movement * 4.5
    if angle < -90:
        angle = -90
    # img = pygame.transform.rotozoom(bird[bird_index], angle, 1)  # filtered
    img = pygame.transform.rotate(bird[bird_index], angle)
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
    text_rect = text.get_rect(midtop=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 7))
    shadow = game_font2.render(str(score), True, (0, 0, 0))
    shadow_rect = shadow.get_rect(midtop=(SCREEN_WIDTH / 2 + 1, SCREEN_HEIGHT / 7))

    screen.blit(shadow, shadow_rect)
    screen.blit(text, text_rect)


def draw_message(game_state):
    if game_state == START:
        get_ready_rect = get_ready.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5))
        tap_rect = tap.get_rect(center=(SCREEN_WIDTH / 2, BIRD_START_Y))

        screen.blit(get_ready, get_ready_rect)
        screen.blit(tap, tap_rect)


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
        return GAME_OVER
    return PLAYING


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
def load_image(filename, scale2):
    img = pygame.image.load('assets/' + filename + '.png').convert_alpha()
    return pygame.transform.scale(img,
                                  (round(img.get_width() * SCALE * scale2), round(img.get_height() * SCALE * scale2)))


# Images
bg = load_image('background-day', 1)
floor = load_image('base', 1)
bird_colour = random.choice(['red', 'blue', 'yellow'])
bird = [load_image(bird_colour + 'bird-upflap', 1), load_image(bird_colour + 'bird-midflap', 1),
        load_image(bird_colour + 'bird-downflap', 1)]
pipe = load_image('pipe-green', 1)
get_ready = load_image('getready', 2)
tap = load_image('tap', 2)

# Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collide_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# Rendering constants
BIRD_X = SCREEN_WIDTH / 3
BIRD_START_Y = SCREEN_HEIGHT / 2

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
pygame.time.set_timer(FLAP, 100)
HOVER = pygame.event.custom_type()
pygame.time.set_timer(HOVER, 200)

# Pipe variables
pipe_rects = []
SPAWN_PIPE = pygame.event.custom_type()
pygame.time.set_timer(SPAWN_PIPE, 1300)     # TODO: resizable original: 1200

# Floor x pos
floor_x = 0

# Score
score = 0

# Game state
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START


def draw():
    screen.blit(bg, (0, 0))
    draw_pipes(pipe_rects)
    draw_floor(floor_x)
    draw_bird(bird_index, bird_rect, movement)
    draw_score()
    draw_message(game_state)


while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state != GAME_OVER:
            if event.type == pygame.KEYDOWN:        # could just make any key the command
                if event.key == pygame.K_SPACE:
                    movement = -JUMP
                    flap_sound.play()
                    game_state = PLAYING

            if event.type == FLAP:
                bird_index = (bird_index + 1) % 3       # 3 frames
        if event.type == HOVER:     # TODO: hovering
            if movement == 0:
                movement += 5 * GRAVITY
            else:
                movement -= 5 * -GRAVITY

        if event.type == SPAWN_PIPE and game_state == PLAYING:
            pipe_rects.extend(load_pipe_rects())

        if game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = START
                    bird_rect.centery = BIRD_START_Y
                    movement = 0
                    pipe_rects.clear()
                    score = 0
# if bird_rect has not touched the floor and game_state is not START, then update bird_rect position
    if bird_rect.bottom < FLOOR_Y - 15 and game_state != START:
        # update bird rect
        movement += GRAVITY
        bird_rect.centery += movement
    elif game_state == PLAYING:
        game_state = GAME_OVER


    if game_state == PLAYING:
        # check collision
        game_state = check_collision(bird_rect, pipe_rects)

        # update score
        check_score(pipe_rects)

        # scroll pipes
        pipe_rects = move_pipes(pipe_rects)

    if game_state != GAME_OVER:
        # scroll floor
        floor_x -= SCROLL_SPEED
        if floor_x <= -floor.get_width():
            floor_x = 0
    else:        # pause the scrolling and let the bird hit the ground if it hasn't already
        pass

    draw()
    pygame.display.update()
    pygame.time.Clock().tick(60)
