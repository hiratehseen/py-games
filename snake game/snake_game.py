import pygame
import random
import os
# pygame initialize
pygame.init()
# music load
pygame.mixer.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
purple = (51, 0, 25)

# game window
width = 700
height = 500
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
pygame.display.update()

# back ground image
image = pygame.image.load("snake.jpg")
# convert_alpha function to maintain speed in game that's effected by image
image = pygame.transform.scale(image, (width, height)).convert_alpha()

# clock
clock = pygame.time.Clock()
# font of score
font = pygame.font.SysFont(None, 35)  # take arguments 1 default font of system and size of font


# font function
def score_on_screen(text, color, x, y):
    """
    render take different arguments, 2nd argument of render function is antialias that's use to little bit
    set high resolution in low resolution
    """
    screen_text = font.render(text, True, color)
    # blit function use update screen
    game_window.blit(screen_text, (x, y))


# make snake
def plot_snake(g_window, color, snk_list, snk_size):
    for x, y in snk_list:
        pygame.draw.rect(g_window, color, [x, y, snk_size, snk_size])


# welcome screen function
def welcome_screen():
    exist = False
    while not exist:
        game_window.fill(purple)
        score_on_screen("Welcome to Snake", white, width/3, height/3)
        score_on_screen("Press 'Space' to Continue", white, width/3.5, height/2.5)
        for event in pygame.event.get():  # handle all the events
            if event.type == pygame.QUIT:
                exist = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("screen.mp3")
                    pygame.mixer.music.play()
                    game_loop()

        pygame.display.update()
        clock.tick(60)


# game loop function
def game_loop():
    # game specific variable
    exist = False
    over = False
    # set snake
    snake_x = 45
    snake_y = 55
    snake_size = 10
    fps = 60  # frame per second
    # check file if not exist
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")

    # high score file
    with open("high_score.txt", "r") as f:
        high_score = f.read()
    # snake specifications
    velocity_x = 0
    velocity_y = 0
    score = 0
    init_velocity = 5
    snake_length = 1
    # snake variables
    snake_list = []
    # food
    apple_x = random.randint(20, width / 2)
    apple_y = random.randint(20, height / 2)
    # game loop
    while not exist:
        if over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            game_window.fill(purple)
            score_on_screen("Game over press 'Enter' to continue", white, (width-450)/2, (height-200)/2)
            for event in pygame.event.get():  # handle all the events
                # print(event)
                if event.type == pygame.QUIT:
                    exist = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome_screen()
        else:
            for event in pygame.event.get():  # handle all the events
                # print(event)
                if event.type == pygame.QUIT:
                    exist = True
                if event.type == pygame.KEYDOWN:
                    # keys actions
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_r:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_l:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_u:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN or event.key == pygame.K_d:
                        velocity_y = init_velocity
                        velocity_x = 0

            # set x,y direction velocity
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - apple_x) < 6 and abs(snake_y - apple_y) < 6:
                score += 10
                # print("Score: ", score * 10)
                # change food space
                apple_x = random.randint(20, width / 2)
                apple_y = random.randint(20, height / 2)
                snake_length += 5
                if score > int(high_score):
                    high_score = score

            # change the color of screen
            game_window.fill(white)
            game_window.blit(image, (0, 0))
            # use string for concatenation
            # coordinates increase and snake length change
            score_on_screen("Score: " + str(score) + "          High Score: " + str(high_score), red, 5, 5)
            # append snake in head otherwise snake not show
            head = [snake_x, snake_y]
            # head.append(snake_x)
            # head.append(snake_y)
            snake_list.append(head)

            # when head increase then its first element delete otherwise snake increases in loop
            # snake length not increase from length
            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[: -1]:
                over = True
                pygame.mixer.music.load("over.mp3")
                pygame.mixer.music.play()
            # game over
            if snake_x < 0 or snake_x > width or snake_y < 0 or snake_y > height:
                over = True
                pygame.mixer.music.load("over.mp3")
                pygame.mixer.music.play()
            # draw snake
            plot_snake(game_window, red, snake_list, snake_size)
            # draw apple
            pygame.draw.rect(game_window, white, [apple_x, apple_y, snake_size, snake_size])
        # apply any change in screen run update function
        pygame.display.update()
        # clock per second
        clock.tick(fps)

    # quit game and python
    pygame.quit()
    quit()


welcome_screen()
# game_loop()
