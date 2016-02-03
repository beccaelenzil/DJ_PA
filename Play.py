import pygame
import spritesheet
import SpriteStripAnim
import sys
import pytmx
import time
import pyglet

from pygame.locals import Color
from pytmx.util_pygame import load_pygame

class Play():
    def __init__(self, screen):

        #pygame.init()

        self.screen = screen

        self.black = Color('Black')

        self.playerspritesheet = spritesheet.spritesheet("AstronautSpriteAtlas.bmp")

        self.clock = pygame.time.Clock()

        self.facingright = True
        self.movingright = False
        self.movingleft = False
        self.movingup = False
        self.movingdown = False
        self.jumping = False
        self.playervelocity = 100

        self.playerx = 320
        self.playery = 240

        self.changex = 0
        self.changey = 0

        self.idleimage = self.playerspritesheet.image_at((5, 84, 15, 32), colorkey=(129, 129, 129))
        self.gunimage = self.playerspritesheet.image_at((77, 92, 24, 9), colorkey=(129, 129, 129))
        self.armimage = self.playerspritesheet.image_at((57, 98, 12, 5), colorkey=(129, 129, 129))

        self.jumpSound = pyglet.resource.media('Jump.wav', streaming=False)

        # All the screen stuff
        pygame.display.set_caption("Play State")

    def calculate_gravity(self):
        if self.changey == 0:
            self.changey = 1
        else:
            self.changey += .35

        # Check if the player is on the ground
        if self.playery >= 480 - 32 and self.changey >= 0:
            self.changey = 0
            self.playery = 480 - 32

    def jump(self):
        if self.playery >= 480:
            self.changey = -10


    def run(self):
        mainLoop = True
        while mainLoop:

            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainLoop = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movingleft = False
                        self.movingright = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movingleft = False
                        self.movingright = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movingdown = False
                        self.movingup = False
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movingup = False
                        self.movingdown = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if self.facingright == True:
                            self.idleimage = pygame.transform.flip(self.idleimage, True, False)
                            self.gunimage = pygame.transform.flip(self.gunimage, True, False)
                            self.armimage = pygame.transform.flip(self.armimage, True, False)
                            self.facingright = False
                            self.movingright = False
                            self.movingleft = True
                        else:
                            self.movingleft = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if self.facingright == False:
                            self.idleimage = pygame.transform.flip(self.idleimage, True, False)
                            self.gunimage = pygame.transform.flip(self.gunimage, True, False)
                            self.armimage = pygame.transform.flip(self.armimage, True, False)
                            self.facingright = True
                            self.movingleft = False
                            self.movingright = True
                        else:
                            self.movingright = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.movingdown == False:
                            self.movingup = False
                            self.movingdown = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movingup = True
                        self.movingdown = False
                        self.jumpSound.play()
                    if event.key == pygame.K_SPACE:
                        self.jumping = True
            if self.movingright == True:
                self.playerx += 5
            elif self.movingleft == True:
                self.playerx -= 5
            if self.movingup == True:
                self.playery -= 5
            elif self.movingdown == True:
                self.playery += 5

            self.screen.fill(self.black)
            self.playery += self.changey

            self.calculate_gravity()

            self.screen.blit(self.idleimage, (self.playerx, self.playery))

            if self.facingright == True:
                self.screen.blit(self.armimage, (self.playerx + 8, self.playery + 15))
            else:
                self.screen.blit(self.armimage, (self.playerx - 4, self.playery + 15))

            # Update the screen's rendering
            pygame.display.flip()

        #one issue I found was the indentation level of this pygame.quit() - Becca 1/27
        #indenting fixed the quit issue, but introduces other issues
    pygame.quit()

if __name__ == "__main__":
    pygame.init()