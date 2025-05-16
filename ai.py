"""
Alien Invasion
Austin Pace
04/23/2025

history:
20250423-001 Initial game setup with screen and ship
20250423-002 Implemented keyboard controls for ship movement
20250423-003 Added bullet firing mechanism
20250423-004 Created alien fleet with movement patterns
20250423-005 Implemented collision detection
20250423-006 Added game statistics tracking
20250423-007 Implemented start/game over screens
20250423-008 Finalized game balancing
20250423-009 Adjusted ship/alien sizes and counts
20250423-010 Added vertical ship movement
20250423-011 Unlimited yellow bullets with faster speed
20250423-012 Randomized alien speeds and crossing behavior
20250423-013 Progressive difficulty with increasing alien waves
20250423-014 Modified game over conditions
20250423-015 Refined alien behavior
20250423-016 Simplified alien spawning
20250423-017 Fix range error
20250423-018 Change ship speed and alien
20250423-019 Aliens follow ship
20250423-020 Add SFX and music
20250423-021 Add explosion file
20250423-022 Change ship lives to 1 from 3 and create Game Over screen
20250423-023 Add fullscreen mode
20250423-024 Fullscreen boundary fix
20250423-025 Update to alien waves/stages
20250423-026 Add death sequence
"""

import sys
import pygame
import random
import math
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from gamestats import GameStats
from explosion import Explosion

class AlienInvasion:
    #20250423-001 Start - Initial game setup
    def __init__(self):
        """Initialize the game,and create game resources"""
        pygame.init()
        #20250423-020 Start - Add SFX and music
        pygame.mixer.init()
        
        self.laser_sound = pygame.mixer.Sound('laser.mp3')
        self.explosion_sound = pygame.mixer.Sound('explosion.mp3')
        self.laser_sound.set_volume(0.2)
        self.explosion_sound.set_volume(0.1)
        
        self.lobby_music = 'lobby.mp3'
        self.game_over_music = 'game_over.mp3'
        self.current_music = None
        #20250423-020 End

        self.settings = Settings()
        
        #20250423-009 Start - Adjusted screen size
        self.screen = pygame.display.set_mode((self.settings.windowed_width,self.settings.windowed_height))
        pygame.display.set_caption('ALIEN INVASION')
        
        #20250423-006 Start - Game statistics
        self.stats = GameStats(self)
        self.ship = Ship(self)
        
        #20250423-004 Start - Alien fleet management
        self.bullets = Group()
        self.aliens = Group()
        
        #20250423-021 Start - Add explosion file
        self.explosions = Group()
        #20250423-021 End

        self.stage_2_explosions = []
        self.waiting_for_explosions = False

        #20250423-007 Start - Game state control
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.last_alien_spawn = pygame.time.get_ticks()
        self.alien_spawn_interval = 2000
        self.wave_count = 0
        self.formation_intact = True

        #20250423-018 Start
        self.settings.ship_speed *= 2  
        self.max_aliens = 8
        #20250423-018 End  

        #20250423-026 Start - Add death sequence
        self.death_sound = pygame.mixer.Sound('death.mp3') 
        self.death_timer = 0
        self.death_animation_frames = 25
        self.ship_visible = True
        self.death_in_progress = False
        #20250423-026 End

        #20250423-020
        self.game_active = False
        self.play_music(self.lobby_music)
    #20250423-001 End

    def play_music(self,music_file,loops=-1):
        """Play music file with optional looping"""
        if self.current_music != music_file:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(loops=loops)
            pygame.mixer.music.set_volume(0.25)
            self.current_music = music_file

    #20250423-023 Start - Add fullscreen mode
    def toggle_fullscreen(self):
        """Properly handle fullscreen/windowed transitions"""
        #20250423-024 Start - Fullscreen boundary update
        self.settings.fullscreen = not self.settings.fullscreen
    
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.windowed_width,self.settings.windowed_height))
            self.settings.screen_width = self.settings.windowed_width
            self.settings.screen_height = self.settings.windowed_height
        
        self.ship.screen_rect = self.screen.get_rect()
        self.ship.center_ship()
        #20250423-024 End
    #20250423-023 End

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self.check_events()
            
            if self.game_active:
                if self.death_in_progress:
                    self.update_death_animation()
                else:
                    self.ship.update()
                    self.update_bullets()
                    self.update_aliens()
                    self.update_explosions()
                    
                    if self.waiting_for_explosions:
                        self.check_explosions_complete()
                    
                    if not self.formation_intact:
                        self.spawn_aliens()
            
            self.update_screen()
            self.clock.tick(60)

    def update_explosions(self):
        """Update explosion animations"""
        for explosion in self.explosions.copy():
            if explosion.update(): 
                self.explosions.remove(explosion)

    #20250423-002 Start - Keyboard controls (expanded in 010)
    def check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
    #20250423-002 End

    #20250423-010 Start - Vertical movement addition
    def check_keydown_events(self,event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self.fire_bullet()
            else:
                self.start_game()
        elif event.key == pygame.K_f: 
            self.toggle_fullscreen()
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self,event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False
    #20250423-010 End

    #20250423-007 Start - Game state management
    def start_game(self):
        """Start a new game"""
        self.stats.reset_stats()
    
        self.aliens.empty()
        self.bullets.empty()
        self.explosions.empty()
        
        self.create_initial_fleet()
        self.ship.center_ship()

        self.game_active = True
        self.formation_intact = True
        
        pygame.mixer.music.stop()
    #20250423-007 End

    #20250423-011 Start - Unlimited yellow bullets
    def fire_bullet(self):
        """Create a new bullet"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        self.laser_sound.play()
    #20250423-011 End

    def update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self.check_bullet_alien_collisions()

    #20250423-005 Start - Collision detection
    def check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
    
        if collisions:
            for aliens_hit in collisions.values():
                for alien in aliens_hit:
                    explosion = Explosion(self,alien.rect.center)
                    self.explosions.add(explosion)
                    self.explosion_sound.play()
                    
                    if self.stats.level == 2:
                        self.stage_2_explosions.append(explosion)
                
                self.stats.aliens_destroyed += len(aliens_hit)
                
                if len(self.aliens) == 0:
                    if self.stats.level == 2:
                        self.waiting_for_explosions = True
                    else:
                        self.start_new_wave()
#20250423-005 End

#20250423-025 Start - Update to alien waves/stages
    def start_new_wave(self):
        """Start a new wave of aliens"""
        self.stats.level += 1
        self.stats.wave_cleared = False
        self.formation_intact = True
        self.wave_count += 1
        
        if self.stats.level == 3:
            alert_font = pygame.font.Font('Grand9k Pixel.ttf',72)
            alert_text = alert_font.render("ALIENS ARE ATTACKING!",True,(255,0,0))
            self.screen.blit(alert_text,(self.settings.screen_width//2 - alert_text.get_width()//2,self.settings.screen_height//2))
            pygame.display.flip()
            pygame.time.delay(1500)   

        if self.settings.alien_min_speed < self.settings.alien_base_max_speed:
            self.settings.alien_min_speed = min(self.settings.alien_min_speed * self.settings.alien_speed_increase,self.settings.alien_base_max_speed)
            self.settings.alien_max_speed = min(self.settings.alien_min_speed * 1.5,self.settings.alien_base_max_speed)
        
        self.create_initial_fleet()
        
        pygame.mixer.Sound('wave.mp3').play()

    def check_stage_2_cleared(self):
        """Wait for all explosions to finish before stage 3"""
        self.stage_2_explosions = [exp for exp in self.stage_2_explosions if not exp.finished]
    
        if not self.stage_2_explosions:
            self.stats.level()
            self.start_new_wave()

    def check_explosions_complete(self):
        """Check if all stage 2 explosions have finished"""
        if not self.waiting_for_explosions:
            return
            
        self.stage_2_explosions = [exp for exp in self.stage_2_explosions if not exp.finished]
        
        if not self.stage_2_explosions: 
            self.waiting_for_explosions = False
            self.start_new_wave()

    def show_stage_3_warning(self):
        """Display stage 3 transition warning"""
        warning_font = pygame.font.Font('Grand9K Pixel',72)
        warning_text = warning_font.render("ALIENS ARE ATTACKING!",True,(255,0,0))
        text_rect = warning_text.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2))
        
        self.screen.blit(warning_text,text_rect)
        pygame.display.flip()
        pygame.time.delay(1500)
    #20250423-025 End

    #20250423-014 Start - Modified alien update
    #20250423-014 Start - Modified alien update
    def update_aliens(self):
        """Update alien positions with bounds checking"""
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self.ship_hit()
        
        aliens_to_remove = []
        for alien in self.aliens.sprites():
            alien.update()
            if alien.rect.top > self.settings.screen_height:
                aliens_to_remove.append(alien)
        
        for alien in aliens_to_remove:
            self.aliens.remove(alien)
            if self.stats.level >= 3: 
                self.create_alien()
    #20250423-014 End

    #20250423-008 Start - Game over conditions
    def ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.death_in_progress:
            return
            
        self.death_in_progress = True
        self.death_timer = 0
        self.ship_visible = True
        self.death_sound.play()
        pygame.mixer.music.fadeout(1000)  
    #20250423-008 End

    def update_death_animation(self):
        """Handle ship death animation"""
        if not self.death_in_progress:
            return
            
        self.death_timer += 1
        
        if self.death_timer % 5 == 0:
            self.ship_visible = not self.ship_visible
            
        if self.death_timer >= self.death_animation_frames * 5:
            self.death_in_progress = False
            self.game_active = False
            self.play_music(self.game_over_music)

    #20250423-004 Start - Alien fleet creation
    #20250423-016 Start - Simplify fleet
    def create_initial_fleet(self):
        """Create wave-specific formations"""
        if self.stats.level <= 2:
            for row in range(2):
                for col in range(4):
                    alien = Alien(self)
                    alien.x = 150 + col * 200
                    alien.y = 50 + row * 150
                    alien.rect.x = alien.x
                    alien.rect.y = alien.y
                    self.aliens.add(alien)
        else:
            for _ in range(8):
                self.create_alien()
    #20250423-016 End

    #20250423-013 Start - Progressive difficulty
    def spawn_aliens(self):
        """Continuously spawn aliens with increasing difficulty"""
        if not self.stats.wave_cleared:
            return
            
        now = pygame.time.get_ticks()
        if now - self.last_alien_spawn > self.alien_spawn_interval:
            self.last_alien_spawn = now
            
            aliens_to_spawn = min(1 + self.wave_count // 3,self.max_aliens - len(self.aliens))
            
            for _ in range(aliens_to_spawn):
                self.create_alien()
            
            self.stats.wave_cleared = False  
    #20250423-013 End

    #20250423-012 Start - Randomized alien behavior
    #20250423-016 Start - Simplified alien system
    #20250423-017 Start - Fix range error
    def create_alien(self):
        """Create individual aliens with proper wave-based positioning"""
        alien = Alien(self)
        
        if self.stats.level >= 3:
            alien.rect.x = random.randint(0,self.settings.screen_width - alien.rect.width)
            alien.rect.y = random.randint(-150,-alien.rect.height)
            alien.x = float(alien.rect.x)
            alien.y = float(alien.rect.y)
        
        self.aliens.add(alien)
        #20250423-012 End
        #20250423-016 End
        #20250423-017 End

    #20250423-007 Start - Screen updates
    def update_screen(self):
        """Update images on the screen,and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
    
        if self.game_active:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet() 

            self.aliens.draw(self.screen)
            self.explosions.draw(self.screen)
            
           
            if not self.death_in_progress or self.ship_visible:
                self.ship.blitme()
                
            self.show_stats()
        else:
            if self.stats.aliens_destroyed > 0:
                self.show_game_over()
            else:
                self.show_menu()
        
        pygame.display.flip()

    def show_menu(self):
        """Display the start menu"""
        font = pygame.font.Font('Grand9k Pixel.ttf',64)
        title = font.render('ALIEN INVASION',True,(119,37,16))
        title_rect = title.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//3))
        
        font = pygame.font.Font('Grand9k Pixel.ttf',36)
        instruction = font.render('Press SPACE to Start',True,(242,189,205))
        instruction_rect = instruction.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2))

        fullscreen_info = font.render('Press F to toggle Fullscreen',True,(242,189,205))
        fullscreen_rect = instruction.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2 + 50))

        quit_info = font.render('Press Q to Quit the Game',True,(242,189,205))
        quit_rect = instruction.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2 + 100))

        creator_info = font.render('created by Austin Pace',True,(242,189,205))
        creator_rect = instruction.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2 + 175))

        label_info = font.render('code.sif, 2025',True,(242,189,205))
        label_rect = instruction.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2 + 225))
        
        self.screen.blit(title,title_rect)
        self.screen.blit(instruction,instruction_rect)
        self.screen.blit(fullscreen_info,fullscreen_rect)
        self.screen.blit(quit_info,quit_rect)
        self.screen.blit(creator_info,creator_rect)
        self.screen.blit(label_info,label_rect)

    def show_game_over(self):
        #20250423-022 Start - Create Game Over screen
        """Display the game over screen"""
        overlay = pygame.Surface((self.settings.screen_width,self.settings.screen_height),pygame.SRCALPHA)
        overlay.fill((0,0,0,200))  

        font_large = pygame.font.Font('Grand9k Pixel.ttf',72)
        game_over = font_large.render('GAME OVER',True,(119,37,16))
        go_rect = game_over.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//3))

        font_medium = pygame.font.Font('Grand9k Pixel.ttf',36)
        stats_text = font_medium.render(f'Aliens Destroyed: {self.stats.aliens_destroyed}',True,(242,189,205))
        stats_rect = stats_text.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height//2))
        
        restart = font_medium.render('Press SPACE to Play Again',True,(255,255,255))
        restart_rect = restart.get_rect(center=(self.settings.screen_width//2,self.settings.screen_height*2//3))
        
        self.screen.blit(game_over,go_rect)
        self.screen.blit(stats_text,stats_rect)
        self.screen.blit(restart,restart_rect)
        #20250423-022 End

    def show_stats(self):
        """Display the game statistics"""
        font = pygame.font.Font('Grand9k Pixel.ttf',24)
        ships = font.render(f'Ships: {self.stats.ships_left}',True,(255,255,255))
        aliens = font.render(f'Aliens Destroyed: {self.stats.aliens_destroyed}',True,(255,255,255))
        wave = font.render(f'Wave: {self.stats.level}',True,(255,255,255))  

        self.screen.blit(ships,(20,20))
        self.screen.blit(aliens,(20,50))
        self.screen.blit(wave,(20,80))  
    #20250423-007 End

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()