import pygame
import spritesheet
from SpriteStripAnim import SpriteStripAnim
import sys
import pytmx
import time
import pyglet

from pygame.locals import Color
from pytmx.util_pygame import load_pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Play():
    def __init__(self, screen):

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
        self.mainLoop = True

        self.playerx = 200
        self.playery = 100

        self.changex = 0
        self.changey = 0

        self.FPS = 120
        self.frames = self.FPS / 12

        self.spritindex = 0

        self.idleimage = self.playerspritesheet.image_at((5, 84, 15, 32), colorkey=(129, 129, 129))
        self.gunimage = self.playerspritesheet.image_at((77, 92, 24, 9), colorkey=(129, 129, 129))
        self.armimage = self.playerspritesheet.image_at((57, 98, 12, 5), colorkey=(129, 129, 129))
        self.jumpingImage = self.playerspritesheet.image_at((30, 85, 17, 31), colorkey=(129, 129, 129))

        self.walkFrames = [
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (7, 30, 15, 35), 1, (129, 129, 129), True, self.frames),
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (103, 0, 15, 32), 1, (129, 129, 129), True, self.frames),
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (71, 0, 15, 32), 1, (129, 129, 129), True, self.frames) +
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (38, 0, 16, 32), 1, (129, 129, 129), True, self.frames),
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (5, 0, 17, 32), 1, (129, 129, 129), True, self.frames),
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (38, 33, 16, 32), 1, (129, 129, 129), True, self.frames) +
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (69, 33, 17, 32), 1, (129, 129, 129), True, self.frames),
            SpriteStripAnim('AstronautSpriteAtlas.bmp', (5, 84, 15, 32), 1, (129, 129, 129), True, self.frames)
        ]

        self.jumpSound = pyglet.resource.media('Jump.wav', streaming=False)
        pygame.mixer.music.load('STG Theme.ogg')

        self.walkFrames[self.spritindex].iter()

        self.titlefont = pygame.font.Font("Brandon_reg.otf", 40)
        self.titlelabel = self.titlefont.render("Welcome to Stellar", 1, WHITE)

    def calculate_gravity(self):
        if self.changey == 0:
            self.changey = 1
        else:
            self.changey += .20

        # Check if the player is on the ground
        if self.playery >= 480 - 32 and self.changey >= 0:
            self.movingup = False
            self.changey = 0
            self.playery = 480 - 32

    def jump(self):
        if self.playery >= 480:
            self.changey = -10


    def run(self):
        while self.mainLoop:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mainLoop = False
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
                    if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.movingdown = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if self.facingright == True:
                            # Flip the image since the player is moving right.
                            self.idleimage = pygame.transform.flip(self.idleimage, True, False)
                            self.gunimage = pygame.transform.flip(self.gunimage, True, False)
                            self.armimage = pygame.transform.flip(self.armimage, True, False)
                            self.jumpingImage = pygame.transform.flip(self.jumpingImage, True, False)
                            self.facingright = False
                            self.movingright = False
                            self.movingleft = True
                        else:
                            self.movingleft = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if self.facingright == False:
                            # Flip the image since the player is facing left.
                            self.idleimage = pygame.transform.flip(self.idleimage, True, False)
                            self.gunimage = pygame.transform.flip(self.gunimage, True, False)
                            self.armimage = pygame.transform.flip(self.armimage, True, False)
                            self.jumpingImage = pygame.transform.flip(self.jumpingImage, True, False)

                            self.facingright = True
                            self.movingleft = False
                            self.movingright = True
                        else:
                            self.movingright = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.movingdown == False:
                            self.movingup = False
                            self.movingdown = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
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

            self.screen.blit(self.titlelabel, (170, 100))

            pygame.mixer.music.play(-1)

            self.walkFrames[self.spritindex].iter()

            if self.movingup == False and self.movingleft == False and self.movingright == False:
                self.screen.blit(self.idleimage, (self.playerx, self.playery))
            elif self.movingup == True:
                self.screen.blit(self.jumpingImage, (self.playerx, self.playery))
            elif self.movingleft == True or self.movingright == True:
                self.spritindex += 1
                if self.spritindex >= len(self.walkFrames):
                    self.spritindex = 0
                self.walkFrames[self.spritindex].iter()

                if self.facingright == True:
                    self.screen.blit(self.walkFrames[self.spritindex].next(), (self.playerx, self.playery))
                else:
                    walkimage = self.walkFrames[self.spritindex].next()
                    self.screen.blit(pygame.transform.flip(walkimage, True, False), (self.playerx, self.playery))

            if self.facingright == True:
                self.screen.blit(self.armimage, (self.playerx + 10, self.playery + 15))
                self.screen.blit(self.gunimage, (self.playerx + 13, self.playery + 10))
            else:
                self.screen.blit(self.armimage, (self.playerx - 4, self.playery + 15))
                self.screen.blit(self.gunimage, (self.playerx - 18, self.playery + 10))

            # Update the screen's rendering
            pygame.display.flip()

            self.clock.tick(self.FPS)

        #one issue I found was the indentation level of this pygame.quit() - Becca 1/27
        #indenting fixed the quit issue, but introduces other issues
    pygame.quit()