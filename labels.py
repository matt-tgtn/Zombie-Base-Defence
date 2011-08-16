#!/usr/bin/env python

############################################
##  Copyright (C) Matt Titterington 2011  ##
##                                        ##
##  Released under the terms of the GNU   ##
##      General Public License. See       ##
##     LICENSE.txt for more details.      ##
############################################

import pygame
from main import load_image

class AmmoCounter(pygame.sprite.Sprite):
    """This class provides a way for the user to know which gun they are using and to see how much ammo they have left
    """
    
    def __init__(self, screenPos, currentGun):
        """
        
        Arguments:
        - `screenPos`: Coordinates of the bottom right corner
        - `currentGun`: BaseGun object of the current gun
        """
        pygame.sprite.Sprite.__init__(self)

        self._screenPos = screenPos
        
        self.initVars(currentGun)
        self.image, self.rect = self.construct()
        self.rect.right = self._screenPos[0]
        self.rect.bottom = self._screenPos[1]

    def __str__(self):
        """
        """
        return 'ammocounter'


    def update(self, currentGun):
        self.initVars(currentGun)
        self.image, self.rect = self.construct()
        self.rect.right = self._screenPos[0]-5
        self.rect.bottom = self._screenPos[1]

    def construct(self):
        """This class will construct the ammo counter
        """
        if self._currentGun == 'm9':
            gunBMP = 'M9icon.bmp'
        elif self._currentGun == 'smg':
            gunBMP = 'SMGicon.bmp'
        elif self._currentGun == 'sniper':
            gunBMP = 'SNIPERicon.bmp'
        gunImage, gunImageRect = load_image(gunBMP)
        


        ammoText = '%s/%s'%(self._currentClip, self._ammo)
        
        textFont = pygame.font.Font(None, 32)
        textSurface = textFont.render(ammoText, True, [0,0,0], [255,255,255])
        textSurfaceRect = textSurface.get_rect()
        textSurfaceRect.left = gunImageRect.width
        textSurfaceRect.centery = gunImageRect.height/float(2)


        surfaceSize = [gunImageRect.width+textSurfaceRect.width,gunImageRect.height]
        displaySurface = pygame.surface.Surface(surfaceSize)
        displaySurface.fill([255,255,255])

        displaySurface.blit(gunImage, [0,0])
        displaySurface.blit(textSurface, textSurfaceRect)
        displaySurface.set_colorkey(displaySurface.get_at((0,0))[:3])

        return displaySurface, displaySurface.get_rect()

    def initVars(self, currentGun):
        """
        """
        self._currentGun = currentGun.__str__()
        self._currentClip = currentGun.currentClip
        self._ammo = currentGun.ammo

