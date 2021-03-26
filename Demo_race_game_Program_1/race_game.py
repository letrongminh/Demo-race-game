# import required packages
import pygame
import time
import random

pygame.init()

# Global Variables
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
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

player_width = 68

# set the screen size
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Race')
clock = pygame.time.Clock()

# required audio files
crash_sound = pygame.mixer.Sound("gallery/audio/crash.wav")
power_up = pygame.mixer.Sound("gallery/audio/Powerup.wav")
police_hit = pygame.mixer.Sound("gallery/audio/hit.wav")
dead = pygame.mixer.Sound("gallery/audio/dead.wav")
point = pygame.mixer.Sound("gallery/audio/point.wav")

# required sprites
BACKGROUND = pygame.image.load('gallery/sprites/background_n.png').convert()
DC = pygame.image.load('gallery/sprites/minh_and_ilia.png').convert_alpha()
virus = pygame.image.load('gallery/sprites/virus.png').convert_alpha()
health = pygame.image.load('gallery/sprites/health.png').convert_alpha()
blank = pygame.image.load('gallery/sprites/blank.jpg').convert_alpha()
police = pygame.image.load('gallery/sprites/police.png').convert_alpha()
PLAYER = pygame.image.load('gallery/sprites/user11.png').convert_alpha()

game_Icon = pygame.image.load('gallery/sprites/user11.png')
pygame.display.set_icon(game_Icon)


# shows PLAYER strength value
def things_dodged(count):
    font = pygame.font.SysFont("Times New Roman", 15)
    text = font.render("  STRENGTH   " + str(count), True, bright_red)
    gameDisplay.blit(text, (12, 5))


# displays any objects if we need
def things(thing_x, thing_y, thing_w, thing_h, color):
    pass
    # virus = pygame.image.load('virus.png').convert()
    # pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


# set the PLAYER position
def player(x, y):
    gameDisplay.blit(PLAYER, (x, y))


# display any text objects
def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# action when PLAYER touch virus or corners
def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    time.sleep(2)

    pygame.mixer.music.load('gallery/audio/dead.wav')
    pygame.mixer.music.play(-1)

    largeText = pygame.font.SysFont("Times New Roman", 88)
    TextSurf, TextRect = text_objects("YOU ARE DEAD!", largeText, black)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)

        button("Play Again", (display_width / 2) - 250, 600, 100, 50, green, bright_green, game_loop)
        button("Quit", (display_width / 2) + 250-100, 600, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


# required buttons
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


# close the game
def quitgame():
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

    largeText = pygame.font.SysFont("comicsansms", 50)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unpause()

        # gameDisplay.fill(white)
        button("Continue", (display_width / 2) - 250, 450, 100, 50, green, bright_green, unpause)
        button("Quit", (display_width / 2) + 250-100, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


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
            # print(event)
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(black)
        gameDisplay.blit(DC, ((display_width / 2)-638/2, 30))
        large_Text = pygame.font.SysFont("Cooper Black", 80)
        Text_Surf, Text_Rect = text_objects("Stay away from COVID", large_Text, white)
        Text_Rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(Text_Surf, Text_Rect)

        button("GO!", (display_width / 2) - 250, 600, 100, 50, green, bright_green, game_loop)
        button("Quit", (display_width / 2) + 250-100, 600, 100, 50, red, bright_red, quitgame)

        # pygame.draw.rect(gameDisplay, red, (550, 450, 100, 50))
        pygame.display.update()
        clock.tick(15)


# GAME SECTION
def game_loop():

    global pause

    pygame.mixer.Sound.play(point)
    pygame.mixer.music.stop()
    time.sleep(1)

    pygame.mixer.music.load('gallery/audio/jazz.wav')
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    # virus object details

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 90
    thing_height = 75

    # thingCount = 1

    # health object details

    health_startx = random.randrange(0, display_width)
    health_starty = -600
    health_width = 52
    health_height = 74
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

    Game_Exit = False
    bgY = 0
    player_safe = False
    health_checkpoint = 0

    health_status = False

    police_status = False

    # entire game loop
    while not Game_Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

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

        if bgY < BACKGROUND.get_width() * -1:  # If our bg is at the -width then reset its position
            bgY = 0

        gameDisplay.blit(BACKGROUND, (0, bgY))

        bgY -= 2  # Move both background images back

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
            if thing_startx < x < thing_startx + thing_width and player_safe is False \
                    or thing_startx < x + player_width < thing_startx + thing_width \
                    and player_safe is False:
                # print('x crossover')
                crash()

        # when PLAYER touches police
        if y < police_starty + police_height:  # player crossed police w.r.t Y-axis

            # player crossed police w.r.t X-axis
            if police_startx < x < police_startx + police_width and police_status \
                    or police_startx < x + player_width < police_startx + police_width \
                    and police_status:
                police_fire()

                ############
                pygame.mixer.music.load('gallery/audio/jazz.wav')
                pygame.mixer.music.play(-1)
                ############

                dodged = int(dodged / 1.5)

                police_status = False
                # police_starty = -600

        # when PLAYER touches health
        if y < health_starty + health_height:  # player crossed health w.r.t Y-axis

            # player crossed health w.r.t X-axis
            if health_startx < x < health_startx + health_width and health_status \
                    or health_startx < x + player_width < health_startx + health_width \
                    and health_status:
                # print('health_x crossover')
                power()

                pygame.mixer.music.load('gallery/audio/jazz.wav')
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


# Let's start our COVID Race Game
game_intro()
game_loop()
quitgame()
