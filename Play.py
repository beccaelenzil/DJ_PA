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
GREEN = (0, 255, 0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        self.bulletsheet = spritesheet.spritesheet("bullets.bmp")
        self.bulletrightimage = self.bulletsheet.image_at((208, 1, 16, 13), colorkey=WHITE)
        self.rect = self.bulletsheet.rect
        self.rect.x = 0
    def update(self):
        self.rect.x += 6
        #print self.rect.x
        #print "The bullet is being updated."

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Platform, self).__init__()

        self.width = width
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Play():
    def __init__(self, screen):

        self.screen = screen


        self.black = Color('Black')

        self.playerspritesheet = spritesheet.spritesheet("AstronautSpriteAtlas.bmp")
        self.crystalspritesheet = spritesheet.spritesheet("hud.bmp")

        self.platformlist = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.facingright = True
        self.movingright = False
        self.movingleft = False
        self.movingup = False
        self.movingdown = False
        self.jumping = False
        self.playervelocity = 100
        self.mainLoop = True
        self.shooting = False

        self.collision1 = False
        self.collosion2 = False
        self.collision3 = False

        self.playerx = 200
        self.playery = 100

        self.changex = 0
        self.changey = 0

        self.FPS = 120
        self.frames = self.FPS / 12

        self.score = 0

        self.spritindex = 0
        self.crystalindex = 0

        self.idleimage = self.playerspritesheet.image_at((5, 84, 15, 32), colorkey=(129, 129, 129))
        self.gunimage = self.playerspritesheet.image_at((77, 92, 24, 9), colorkey=(129, 129, 129))
        self.armimage = self.playerspritesheet.image_at((57, 98, 12, 5), colorkey=(129, 129, 129))
        self.jumpingImage = self.playerspritesheet.image_at((30, 85, 17, 31), colorkey=(129, 129, 129))

        self.crystalimage = self.crystalspritesheet.image_at((80, 0, 16, 16), colorkey=WHITE)

        self.scoreFont = pygame.font.Font("Brandon_reg.otf", 20)

        self.level = [[210, 30, 100, 300],
                      [210, 30, 200, 400],
                      [210, 30, 400, 330],
                      [210, 30, 350, 250]]

        for platform in self.level:
                block = Platform(platform[0], platform[1])
                block.rect.x = platform[2]
                block.rect.y = platform[3]
                self.platformlist.add(block)

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

        self.crystalframes = [
            SpriteStripAnim('crystal.bmp', (0, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (16, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (31, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (48, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (64, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (79, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (96, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (111, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (127, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (143, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (159, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (176, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (192, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (208, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (223, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (240, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (255, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (271, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (288, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (303, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (319, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (335, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (352, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (368, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (383, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (400, 0, 16, 16), 1, WHITE, True, self.frames),
            SpriteStripAnim('crystal.bmp', (415, 0, 16, 16), 1, WHITE, True, self.frames) +
            SpriteStripAnim('crystal.bmp', (432, 0, 16, 16), 1, WHITE, True, self.frames)
        ]

        self.jumpSound = pyglet.resource.media('Jump.wav', streaming=False)
        #self.theme = pyglet.resource.media('STG Theme.ogg', streaming=False)

        self.walkFrames[self.spritindex].iter()

    def calculate_gravity(self):
        if self.changey == 0:
            self.changey = 1
        else:
            self.changey += .20

        # Check if the player is on the ground

        for platform in self.platformlist:
            if (self.playery + 35) <= platform.rect.top \
                    and platform.rect.top - 3 <= (self.playery + 35) <= platform.rect.top + 3 \
                    and self.playerx >= platform.rect.left \
                    and self.playerx <= platform.rect.right and self.changey >= 0:
                self.playery = platform.rect.top - 35
                self.movingup = False
                if self.movingup == False:
                    self.changey = 0

        if self.playery >= 480 - 32 and self.changey >= 0:
            self.movingup = False
            self.changey = 0
            self.playery = 480 - 32

    def jump(self):
        if self.playery >= 480:
            self.changey = -10


    def run(self):

        while self.mainLoop:

            #print "new bullet"

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
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movingup = True
                        self.movingdown = False
                        self.jumping = True
                        self.jumpSound.play()
                    if event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                        self.shooting = True
                        bullettospawn = Bullet()
                        if self.facingright == True:
                            a = 1#do something related to right facing
                        y_bullet = self.playery
                        x_bullet = self.playerx
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

            self.platformlist.draw(self.screen)


            self.platformlist.update()

            self.calculate_gravity()

            #self.theme.play()

            self.walkFrames[self.spritindex].iter()

            self.scoreLabel = self.scoreFont.render("Score: " + str(self.score), 1, WHITE)

            self.screen.blit(self.crystalimage, (250, 40))

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

            self.crystalindex += 1
            if self.crystalindex >= len(self.crystalframes):
                self.crystalindex = 0
            self.crystalframes[self.crystalindex].iter()

            x1 = 300
            y1 = 350
            x2 = 400
            y2 = 200
            x3 = 500

            if (self.playerx < x1+8 and self.playerx > x1-8 and self.playery > y1-8 and self.playery < y1+8):
                self.collision1 = True
                self.score += 1
            elif (self.playerx < x2 + 8 and self.playerx > x2 - 8 and self.playery > y2 - 8 and self.playery < y2 + 8):
                self.collision2 = True
                self.score += 1
            elif (self.playerx < x3 + 8 and self.playerx > x3 - 8 and self.playery > x2 - 8 and self.playery < x2 + 8):
                self.collision3 = True
                self.score += 1

            if self.collision1 == False:
                self.screen.blit(self.crystalframes[self.crystalindex].next(), (300, 350))
            if self.collosion2 == False:
                self.screen.blit(self.crystalframes[self.crystalindex].next(), (400, 200))
            if self.collision3 == False:
                self.screen.blit(self.crystalframes[self.crystalindex].next(), (500, 400))

            self.screen.blit(self.scoreLabel, (270, 35))

            if self.facingright == True:
                self.screen.blit(self.armimage, (self.playerx + 10, self.playery + 15))
                self.screen.blit(self.gunimage, (self.playerx + 13, self.playery + 10))
                #bullettospawn = Bullet()
                if self.shooting == True:
                    #bullettospawn = Bullet(self.playerx,self.playery)
                    bullettospawn.update()
                    #self.screen.blit(bullettospawn.bulletrightimage, (self.playerx + 6, self.playery + 6))
                    self.screen.blit(bullettospawn.bulletrightimage, (x_bullet + bullettospawn.rect.x, y_bullet + 6))
            else:
                self.screen.blit(self.armimage, (self.playerx - 4, self.playery + 15))
                self.screen.blit(self.gunimage, (self.playerx - 18, self.playery + 10))
                if self.shooting == True:
                    bullettospawn.update()
                    self.screen.blit(pygame.transform.flip(bullettospawn.bulletrightimage, True, False), (x_bullet - bullettospawn.rect.x, y_bullet + 6))

            # Update the screen's rendering
            self.clock.tick(self.FPS)

            pygame.display.flip()

        #one issue I found was the indentation level of this pygame.quit() - Becca 1/27
        #indenting fixed the quit issue, but introduces other issues
    pygame.quit()