#20250423-009 Start - Adjusted game settings
class Settings:
    """Store all game settings with updated values."""
    
    def __init__(self):
        self.windowed_width = 1200
        self.windowed_height = 800
        self.screen_width = self.windowed_width
        self.screen_height = self.windowed_height
        self.bg_color = (0,0,0)
        self.fullscreen = False
        
        self.ship_speed = 4.0
        #20250423-022 Start - Change ship lives to 1 from 3
        self.ship_limit = 1
        #20250423-022 End

        self.death_animation_duration = 60  
        self.ship_blink_interval = 5

        #20250423-011 Start - Bullet settings
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,0)  
        #20250423-011 End

        #20250423-012 Start - Alien settings
        self.alien_formation_speed = 1.5  
        self.alien_base_min_speed = 1.5
        self.alien_base_max_speed = 4.0
        self.alien_min_speed = self.alien_base_min_speed
        self.alien_max_speed = self.alien_base_min_speed * 1.5  
        self.alien_speed_increase = 1.15
        self.fleet_drop_speed = 10
        self.max_aliens = 8 
        #20250423-012 End

        #20250423-019 Start - Alien attack parameters
        self.alien_attack_range = 400  
        self.alien_direction_change_cooldown = 1000 
        #20250423-019 End
#20250423-009 End