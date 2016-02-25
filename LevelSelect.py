import pygame
import pyglet

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class LevelSelect():
    def __init__(self, screen):
        self.font = pygame.font.Font("Brandon_reg.otf", 30)
        self.screen = screen

    def run(self):
        print "The level select screen is running."
        mainLoop = True
        while mainLoop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False

            clock = pygame.time.Clock()
            clock.tick(60)

            level1label = self.font.render("1", 1, WHITE)
            self.screen.blit(level1label, (100, 100))