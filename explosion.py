#20250423-021 Start - Add explosion file
import pygame
import time

class Explosion(pygame.sprite.Sprite):
    def __init__(self,game,center):
        super().__init__()
        self.finished = False  
        self.game = game
        self.size = 30
        self.image = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        pygame.draw.circle(self.image,(255,0,0),(self.size // 2,self.size // 2),self.size // 2)
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.lifetime = 50
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 50 

    def update(self):
        """Update explosion animation and return True when complete"""
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay:
            self.frame += 1
            self.frame_timer = now
            
            if self.frame < self.lifetime / 2:
                scale = 1 + self.frame / 5
            else:
                scale = 2 - self.frame / 5

            current_size = max(1,int(self.size * scale))
            self.image = pygame.Surface((current_size,current_size),pygame.SRCALPHA)

            green_value = min(255,int((self.frame / self.lifetime) * 255))
            alpha = max(0,255 - int((self.frame / self.lifetime) * 255))
            color = (255,green_value,0,alpha)

            pygame.draw.circle(self.image,color,(current_size // 2,current_size // 2),current_size // 2)
            self.rect = self.image.get_rect(center=self.rect.center)

        if self.frame >= self.lifetime:
            self.finished = True
            return True
        return False
#20250423-021 End