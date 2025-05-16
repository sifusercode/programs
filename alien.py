#20250423-012 Start - Randomized alien behavior
#20250423-019 Start - Aliens follow ship
#20250423-025 Start - Update to alien waves/stages
import pygame
from pygame.sprite import Sprite
import random
import math

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ship = ai_game.ship
        
        self.image = pygame.image.load('alien.png')
        self.rect = self.image.get_rect()

        if self.stats.level >= 3:
            self.rect.x = random.randint(0,self.screen.get_rect().width - self.rect.width)
            self.rect.y = random.randint(-150,-self.rect.height)
        else:
            self.rect.x = 0  
            self.rect.y = 0

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        if self.stats.level <= 2:
            self.speed = self.settings.alien_formation_speed
            self.direction = pygame.math.Vector2(1,0.1)  
        else:
            self.speed = random.uniform(
                self.settings.alien_min_speed * 1.25,
                self.settings.alien_max_speed * 1.25
            )
            self.direction = pygame.math.Vector2(0,1)  
            self.last_direction_change = 0
            self.direction_change_cooldown = 1000  

    def update(self):
        """Update position based on wave"""
        if self.stats.level <= 2:
            self.update_formation_movement()
        else:
            self.update_attack_movement()

        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update_formation_movement(self):
        """Wave 1-2: Synchronized formation movement"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self.direction.x *= -1

    def update_attack_movement(self):
        """Wave 3+: Individual attack patterns"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_direction_change > self.direction_change_cooldown:
            self.last_direction_change = current_time
            
            attack_vector = pygame.math.Vector2(
                self.ship.rect.centerx - self.rect.centerx,
                self.ship.rect.centery - self.rect.centery
            )
            
            if attack_vector.length() > 0:
                attack_vector += pygame.math.Vector2(
                    random.uniform(-0.3,0.3),
                    random.uniform(-0.3,0.3)
                )
                self.direction = attack_vector.normalize()
            
            self.direction_change_cooldown = random.randint(500,1500)
#20250423-012 End
#20250423-019 End 
#20250423-025 End