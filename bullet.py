#20250423-011 Start - Unlimited yellow bullets
import pygame
from pygame.sprite import Sprite

class Bullet(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,
                              self.settings.bullet_height)
        
        self.rect.midtop = game.ship.rect.midtop
        
        self.y = float(self.rect.y)
        
        self.color = self.settings.bullet_color
        self.speed = self.settings.bullet_speed

    def update(self):
        """Move the bullet up the screen"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen,self.color,self.rect)
#20250423-011 End