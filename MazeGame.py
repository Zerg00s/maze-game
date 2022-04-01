# pip install pygame
# pip install pyautoguif
import pygame
import datetime
from datetime import timedelta
import sys
from pathlib import Path
import csv

screen_width, screen_height = 800, 800
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Maze challenge')
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)
screen = pygame.display.set_mode((screen_width, screen_height))


# ==================================== #
#          START MENU
# ==================================== #
base_font = pygame.font.Font(None, 32)
PlayerID = ''

input_rect = pygame.Rect(300, 300, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('gray15')
color = color_passive

playerNameEntered = False
while playerNameEntered == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                playerNameEntered = True
            elif event.key == pygame.K_BACKSPACE:
                PlayerID = PlayerID[:-1]
            else:
                PlayerID += event.unicode
    screen.fill((0, 0, 0))

    msg = base_font.render("Player:", 1, (255, 255, 0))
    screen.blit(msg, (219, 305))

    pygame.draw.rect(screen, color, input_rect, 2)
    text_surface = base_font.render(PlayerID, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.display.flip()
    input_rect.w = max(120, text_surface.get_width()+10)
    clock.tick(60)

# ==================================== #
#          MAZE GAME BEGINS
# ==================================== #
bg = pygame.image.load("game_map.jpg")
bg = pygame.transform.scale(bg, (screen_width, 600))

# Tracking stats
# Participant Number
attempts = 1
# Time until game won in seconds

run = True
font = pygame.font.Font(None, 60)
pygame.mouse.set_pos((25, 650))

font = pygame.font.Font(None, 60)
gameStartTime = datetime.datetime.now()

# TODO: set the mouse cursor to the center of the screen
# pyautogui.moveTo(800, 500)

timeoutDifference = timedelta(seconds=0)
timeoutStartTime = datetime.datetime.now()

while run:
    clock.tick(150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
        0, 0, screen_width, screen_height))
    screen.blit(bg, (0, 150))

    mousePosition = pygame.mouse.get_pos()
    color = screen.get_at(mousePosition)
    print(mousePosition)

    # if color beneath the mouse cursor is re
    if color[0] > 250 and color[1] < 20 and color[2] < 20:
        # You WON
        run = False

    # if color beneath the mouse cursor is black
    if color == (0, 0, 0, 255) and mousePosition != (0, 0):
        pygame.mouse.set_pos((25, 650))

        current_time = datetime.datetime.now()
        if 'timeoutStartTime' in locals():
            timeoutDifference = current_time - timeoutStartTime
        else:
            timeoutDifference = timedelta(seconds=0)

        if timeoutDifference.seconds > 0.5:
            attempts = attempts + 1

        timeoutStartTime = datetime.datetime.now()

    current_time = datetime.datetime.now()
    timeDifference = current_time - gameStartTime

    msg = font.render("Time: " + str(timeDifference.seconds), 1, (00, 00, 255))
    screen.blit(msg, (25, 700))

    attemptsMessage = font.render(
        "Attempts: " + str(attempts), 1, (255, 255, 0))
    screen.blit(attemptsMessage, (25, 750))

    pygame.display.update()

# ==================================== #
#          GAME ENDS
# ==================================== #

run = True
font = pygame.font.Font(None, 100)

while run:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                 # Time to save to CSV
                now = datetime.datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                fields = [PlayerID, attempts, timeoutDifference.seconds, dt_string]
                with open(r'results.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            # Time to save to CSV
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            fields = [PlayerID, attempts, timeoutDifference.seconds, dt_string]
            with open(r'results.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            pygame.quit()
            sys.exit()

    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
        0, 0, screen_width, screen_height))

    msg = font.render("YOU WON!", 1, (255, 255, 0))
    screen.blit(msg, (200, 350))

    pygame.display.update()
