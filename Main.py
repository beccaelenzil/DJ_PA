import sys
import pygame
from Menu import GameMenu
from LevelSelect import LevelSelect
import Play
import pyglet

pygame.init()
pygame.mixer.init()

theme = pyglet.resource.media('STG Theme.ogg', streaming=False)
#theme.play()

mainLoop = True
current_state = "MENU"

screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Stellar")
gameclock = pygame.time.Clock()

def startGame():
    current_state = "PLAY"
    return current_state

i = 0
#class Main():
while mainLoop:

    #print "Doing main game loop"
    gameclock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

        #else:
    # I took this out of the event loop
    funcs = {
        "Start":startGame,
        "Quit":sys.exit
    }

    if current_state == "MENU":
        gameMenu = GameMenu(screen, funcs.keys(), funcs)
        gameMenu.run()
        current_state = startGame()
    elif current_state == "LEVELSELECT":
        levelSelect = LevelSelect(screen)
        levelSelect.run()
    elif current_state == "PLAY":
        theme.play()
        playScreen = Play.Play(screen)
        playScreen.run()
pygame.quit()