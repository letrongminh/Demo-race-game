#!/usr/bin/python
# import required packages
import os
import pygame
import time
import random

pygame.init()

# Global Variables
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
display_width = 1200
display_height = 900
pause = True

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)

player_width = 60

# set the screen size
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Race")
clock = pygame.time.Clock()

# use relative path to resources
file_path = os.path.dirname(__file__)
gallery_path = os.path.join(file_path, "gallery")
sprite_path = os.path.join(gallery_path, "sprites")
audio_path = os.path.join(gallery_path, "audio")

# required audio files
crash_sound = pygame.mixer.Sound(f"{audio_path}/crash.wav")
power_up = pygame.mixer.Sound(f"{audio_path}/Powerup.wav")
police_hit = pygame.mixer.Sound(f"{audio_path}/hit.wav")
dead = pygame.mixer.Sound(f"{audio_path}/dead.wav")
point = pygame.mixer.Sound(f"{audio_path}/point.wav")

# required sprites
BACKGROUND = pygame.image.load(f"{sprite_path}/background_n.png").convert()
DC = pygame.image.load(f"{sprite_path}/front_img.png").convert_alpha()
virus = pygame.image.load(f"{sprite_path}/virus3.png").convert_alpha()
health = pygame.image.load(f"{sprite_path}/health.png").convert_alpha()
blank = pygame.image.load(f"{sprite_path}/blank.jpg").convert_alpha()
police = pygame.image.load(f"{sprite_path}/police.png").convert_alpha()
PLAYER = pygame.image.load(f"{sprite_path}/user11.png").convert_alpha()

game_Icon = pygame.image.load(f"{sprite_path}/user11.png")
pygame.display.set_icon(game_Icon)


# shows PLAYER strength value
def things_dodged(count):
    font = pygame.font.SysFont("Times New Roman", 25)
    text = font.render("  STRENGTH   " + str(count), True, white)
    gameDisplay.blit(text, (12, 5))


# displays any objects if we need
def things(thing_x, thing_y, thing_w, thing_h, color):
    pass


# set the PLAYER position
def player(x, y):
    gameDisplay.blit(PLAYER, (x, y))


# display any text objects
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# action when PLAYER touch virus or corners
def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    time.sleep(2)

    pygame.mixer.music.load(f"{audio_path}/dead.wav")
    pygame.mixer.music.play(-1)

    large_text = pygame.font.SysFont("Times New Roman", 88)
    text_surf, text_rect = text_objects("YOU ARE DEAD!", large_text, white)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surf, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        # gameDisplay.fill(white)
        button("Play Again", (display_width / 2) - 250, 600, 100, 50, green, bright_green, game_loop)
        button("Quit", (display_width / 2) + 250 - 100, 600, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(FPS)


# required buttons
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("Times New Roman", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(text_surf, text_rect)


# close the game
def quit_game():
    pygame.quit()
    quit()


# unpause the game
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


# pause the game
def paused():
    pygame.mixer.music.pause()

    large_text = pygame.font.SysFont("comicsansms", 50)
    text_surf, text_rect = text_objects("Paused", large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surf, text_rect)

    while pause:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unpause()

        # gameDisplay.fill(white)
        button("Continue", (display_width / 2) - 250, 450, 100, 50, green, bright_green, unpause)

        button("Quit", (display_width / 2) + 250 - 100, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(FPS)


# audio when PLAYER touches health
def power():
    pygame.mixer.Sound.play(power_up)
    pygame.mixer.music.stop()


# audio when PLAYER touches police
def police_fire():
    pygame.mixer.Sound.play(police_hit)
    pygame.mixer.music.stop()


# game intro section
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        gameDisplay.fill(white)
        gameDisplay.blit(DC, ((display_width / 2) - 940 / 2, 30))
        large_text = pygame.font.SysFont("Cooper Black", 50)
        text_surf, text_rect = text_objects("The project of Minh and Ilya", large_text, white)
        text_rect.center = ((display_width / 2), (display_height / 2 - 120))
        gameDisplay.blit(text_surf, text_rect)

        button("GO!", (display_width / 2) - 250, 600, 100, 50, green, bright_green, game_loop)

        button("Quit", (display_width / 2) + 250 - 100, 600, 100, 50, red, bright_red, quit_game, )

        pygame.display.update()
        clock.tick(FPS)  # 120 frames per second


# GAME SECTION
def game_loop():
    global pause

    pygame.mixer.Sound.play(point)
    pygame.mixer.music.stop()
    time.sleep(1)

    pygame.mixer.music.load(f"{audio_path}/jazz.wav")
    pygame.mixer.music.play(-1)

    x = display_width * 0.45
    y = display_height * 0.8

    x_change = 0

    # virus object details
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 2
    thing_width = 50
    thing_height = 50

    # thingCount = 1

    # health object details
    health_startx = random.randrange(0, display_width)
    health_starty = -600
    health_width = 50
    health_height = 50
    health_speed = 3

    # police object details

    police_startx = random.randrange(0, display_width)
    police_starty = -600
    police_width = 52
    police_height = 74
    police_speed = 3

    # score
    dodged = 0

    # required variables

    game_exit = False
    background_y = 0
    player_safe = False
    health_checkpoint = 0

    health_status = False

    police_status = False

    # entire game loop
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        if background_y < BACKGROUND.get_width() * -1:  # If our bg is at the -width then reset its position
            background_y = 0

        gameDisplay.blit(BACKGROUND, (0, background_y))

        background_y -= 2  # Move both background images back

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

        gameDisplay.blit(virus, (thing_startx, thing_starty))

        thing_starty += thing_speed

        # display health object only when user scores a minimum of 7
        if dodged % 7 == 0 and dodged != 0 and health_checkpoint == 0:
            health_status = True

        if health_status:
            gameDisplay.blit(health, (health_startx, health_starty))

        health_starty += health_speed

        # display police object only when user scores a minimum of 12

        if dodged % 12 == 0 and dodged != 0:
            police_status = True

        if police_status:
            gameDisplay.blit(police, (police_startx, police_starty))
            # police_starty = -600

        police_starty += police_speed

        # set player poistion
        player(x, y)

        things_dodged(dodged)

        # when user touches the corner
        if x > display_width - player_width or x < 0:
            crash()

        # when virus goes out of the screen
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.5

        # when health object goes out of the screen
        if health_starty > display_height:
            health_starty = 0 - health_height
            health_startx = random.randrange(0, display_width)
            health_speed -= 0.01
            if health_speed < 0:
                health_speed = 0

        # when police object goes out of the screen
        if police_starty > display_height:
            police_starty = -600
            police_startx = random.randrange(0, display_width)

        # when PLAYER touch virus
        if y < thing_starty + thing_height:  # player crossed virus w.r.t to Y-axis
            # print('y crossover')

            # player crossed virus w.r.t X-axis
            if (
                    thing_startx < x < thing_startx + thing_width
                    and player_safe is False
                    or thing_startx < x + player_width < thing_startx + thing_width
                    and player_safe is False
            ):
                # print('x crossover')
                crash()

        # when PLAYER touches police
        if y < police_starty + police_height:  # player crossed police w.r.t Y-axis

            # player crossed police w.r.t X-axis
            if (
                    police_startx < x < police_startx + police_width
                    and police_status
                    or police_startx < x + player_width < police_startx + police_width
                    and police_status
            ):
                police_fire()

                pygame.mixer.music.load(f"{audio_path}/jazz.wav")
                pygame.mixer.music.play(-1)

                dodged = int(dodged / 1.5)

                police_status = False
                # police_starty = -600

        # when PLAYER touches health
        if y < health_starty + health_height:  # player crossed health w.r.t Y-axis

            # player crossed health w.r.t X-axis
            if (
                    health_startx < x < health_startx + health_width
                    and health_status
                    or health_startx < x + player_width < health_startx + health_width
                    and health_status
            ):
                power()

                pygame.mixer.music.load(f"{audio_path}/jazz.wav")
                pygame.mixer.music.play(-1)

                player_safe = True
                health_checkpoint = dodged
                health_status = False

        # when user is in safe mode for next 4 virus objects
        if dodged - health_checkpoint > 4:
            player_safe = False
            health_checkpoint = 0
            health_speed = 3

        # when user comes to unsafe point
        if health_checkpoint > 0:
            gameDisplay.blit(blank, (x, y))
            pygame.display.flip()
            time.sleep(0.01)
            gameDisplay.blit(PLAYER, (x, y))
            pygame.display.flip()

        # update the screen
        pygame.display.update()
        clock.tick(FPS)


game_intro()
game_loop()
quit_game()
