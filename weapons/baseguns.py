#!/usr/bin/env python

############################################
##  Copyright (C) Matt Titterington 2011  ##
##                                        ##
##  Released under the terms of the GNU   ##
##      General Public License. See       ##
##     LICENSE.txt for more details.      ##
############################################

import pygame
import math

class BaseGun:

    damage = 10
    speed = 20
    turnsToFire = 0
    clipSize = 20
    currentClip = 20
    ammo = -1
    reloadTime = 60
    shotTime = 0

    def __init__(self, gunPos, screen, background, bulletGroup):
        self.gunPos = gunPos
        self.bulletGroup = bulletGroup
        
        self.screen = screen
        self.background = background

    def shoot(self, mousePos):
        if self.turnsToFire == 0 and (self.currentClip>0):
            self.turnsToFire = self.shotTime
            self.bulletGroup.add(Bullet(self.damage, self.speed, mousePos, self.gunPos))
            self.currentClip -= 1
    def update(self):
        self.bulletGroup.clear(self.screen,self.background)
        self.bulletGroup.update()
        self.bulletGroup.draw(self.screen)

        if self.turnsToFire > 0:
            self.turnsToFire -= 1

    def reload(self):
        if self.turnsToFire == 0:
            self.turnsToFire = self.reloadTime #reload time = 1 sec
            if not self.ammo == -1:
                if self.ammo>=self.clipSize:
                    self.ammo -= self.clipSize
                    self.currentClip = self.clipSize
                else:
                    self.currentClip = self.ammo
                    self.ammo = 0
            else:
                self.currentClip = self.clipSize
            

class M9(BaseGun):
    damage = 20
    speed = 20
    clipSize = 20
    ammo = -1
    reloadTime = 60
    shotTime = 0
    gunType = 'semi'
    
    def __init__(self, gunPos, screen, background, bulletGroup):
        BaseGun.__init__(self, gunPos, screen, background, bulletGroup)
        self.currentClip = self.clipSize
    def __str__(self):
        """
        """
        return 'm9'


class SMG(BaseGun):
    damage = 10
    speed = 20
    clipSize = 50
    ammo = 200
    reloadTime = 90
    shotTime = 5
    gunType = 'auto'
    
    def __init__(self, gunPos, screen, background, bulletGroup):
        BaseGun.__init__(self, gunPos, screen, background, bulletGroup)
        self.currentClip = self.clipSize 
    def __str__(self):
        """
        """
        return 'smg'


class SNIPER(BaseGun):
    damage = 75
    speed = 20
    clipSize = 5
    ammo = 10
    reloadTime = 300
    shotTime = 120 #Two second shoot time
    gunType = 'semi'
    
    def __init__(self, gunPos, screen, background, bulletGroup):
        BaseGun.__init__(self, gunPos, screen, background, bulletGroup)
        self.currentClip = self.clipSize
    def __str__(self):
        """
        """
        return 'sniper'


        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage, speed, mousePos, bulletOrigin):
        pygame.sprite.Sprite.__init__(self)
        
        self.damage  = damage
        self.speed = speed
        self.pos = bulletOrigin
        
        #Figure out how far to move each time
        relx = float(mousePos[0]-self.pos[0])
        rely = float(mousePos[1]-self.pos[1])
        
        hypotenuse = math.sqrt((relx**2)+(rely**2))
        
        scale = float(speed)/hypotenuse
        
        self.xmove = scale * relx
        self.ymove = scale * rely
        
        
        
        self.image = pygame.surface.Surface([2,2])
        self.image.fill([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self):
        self.pos = (self.pos[0]+self.xmove,self.pos[1]+self.ymove)
        self.rect.center = self.pos
    
