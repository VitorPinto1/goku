import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = (800, 600)
        self.background_image = self.load_background_image('assets/images/pxfuel.jpg')
        
        # Load individual sprite images
        self.sprites = {
            'left': self.load_sprites(['assets/sprites/left.png', 'assets/sprites/right3.png', 'assets/sprites/right5.png']),
            'right': self.load_sprites(['assets/sprites/right1.png', 'assets/sprites/right3.png', 'assets/sprites/right4.png', 'assets/sprites/right5.png']),
            'up': self.load_sprites(['assets/sprites/up.png', 'assets/sprites/uptransparent.png']),
            'down': self.load_sprites(['assets/sprites/down.png', 'assets/sprites/uptransparent.png']),
            'default': self.load_sprites(['assets/sprites/default1.png', 'assets/sprites/default2.png']),
            'ki': [self.load_sprite('assets/sprites/gokut1.png')] + self.load_sprites(['assets/sprites/gokut2.png', 'assets/sprites/gokut3.png']),
            'kame': self.load_sprites(['assets/sprites/k1.png', 'assets/sprites/k2.png', 'assets/sprites/k3.png', 'assets/sprites/k4.png', 'assets/sprites/k5.png', 'assets/sprites/k6.png', 'assets/sprites/k8.png']) 
        }
        
        # Start background music
        pygame.mixer.music.load('assets/sounds/fsdfsdfsdfsd.mp3')
        pygame.mixer.music.play(-1)  # Play indefinitely
       

        self.player_pos = pygame.Vector2(100, 300)
        self.player_speed = 300
        self.current_sprite = 'default'
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.animation_speed = 0.2
        self.kame_animation_speed = 0.6
        
    
        
        self.direction_sprites = {
            pygame.K_q: 'left',  # Images for moving left
            pygame.K_d: 'right',  # Images for moving right
            pygame.K_z: 'up',  # Images for moving up
            pygame.K_s: 'down'  # Images for moving down
        }

        self.sounds = {
            'left': pygame.mixer.Sound('assets/sounds/dbz-teleport.mp3'),
            'right': pygame.mixer.Sound('assets/sounds/dbz-teleport.mp3'),
            'up': pygame.mixer.Sound('assets/sounds/dbz-teleport.mp3'),
            'down': pygame.mixer.Sound('assets/sounds/dbz-teleport.mp3')
        }

        self.ki_key = pygame.K_a
        self.ki_active = False

        self.ki_sound = pygame.mixer.Sound('assets/sounds/gokuyelling.mp3')

        self.kame_key = pygame.K_e
        self.kame_active = False

        self.kame_sound = pygame.mixer.Sound('assets/sounds/kamehameha.swf.mp3')

    def load_background_image(self, path):
        
        try:
            image = pygame.image.load(path).convert()
            image = pygame.transform.scale(image, self.screen_size)
        except pygame.error as e:
            print(f"Error loading image: {path}\n{e}")
            return None
        return image

    def load_sprite(self, path):
       
        try:
            sprite = pygame.image.load(path).convert_alpha()
            original_size = sprite.get_size()
            doubled_size = (original_size[0] * 2, original_size[1] * 2)
            sprite = pygame.transform.scale(sprite, doubled_size)
        except pygame.error as e:
            print(f"Error loading sprite: {path}\n{e}")
            return None
        return sprite
    
    def load_sprites(self, paths):
        
        return [self.load_sprite(path) for path in paths]

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick(60) / 1000  # Delta time in seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.direction_sprites:
                        self.current_sprite = self.direction_sprites[event.key]
                        self.current_frame = 0
                        self.time_since_last_frame = 0
                        self.sounds[self.direction_sprites[event.key]].play()
                        if self.ki_active:  
                            self.ki_active = False
                            self.ki_sound.stop()  
                            self.current_sprite = 'default'  
                        elif self.kame_active:  
                            self.kame_active = False
                            self.kame_sound.stop() 
                            self.current_sprite = 'default'  
                    elif event.key == self.ki_key:
                        if not self.ki_active:  
                            self.current_sprite = 'ki'
                            self.current_frame = 0
                            self.time_since_last_frame = 0
                            self.ki_active = True
                            self.ki_sound.play()
                    elif event.key == self.kame_key:
                        if not self.kame_active:  
                            self.current_sprite = 'kame'
                            self.current_frame = 0
                            self.time_since_last_frame = 0
                            self.kame_active = True
                            self.kame_sound.play()
                elif event.type == pygame.KEYUP:
                    if event.key == self.ki_key:
                        self.ki_active = False
                        self.ki_sound.stop() 
                        self.current_sprite = 'default'  
                        self.current_frame = 0
                        self.time_since_last_frame = 0
                    elif event.key in self.direction_sprites and not self.ki_active:
                        self.current_sprite = 'default'  # Change sprite when ki off
                        self.current_frame = 0
                        self.time_since_last_frame = 0
                elif event.type == pygame.KEYUP:
                    if event.key == self.kame_key:
                        self.kame_active = False
                        self.kame_sound.stop()  
                        self.current_sprite = 'default'  
                        self.current_frame = 0
                        self.time_since_last_frame = 0
                    elif event.key in self.direction_sprites and not self.kame_active:
                        self.current_sprite = 'default'  # change sprite when kame off
                        self.current_frame = 0
                        self.time_since_last_frame = 0  
                elif event.type == pygame.KEYUP:
                    if event.key in self.direction_sprites:
                        # Stop the sound when the key is released
                        self.sounds[self.direction_sprites[event.key]].stop()
                        self.current_sprite = 'default'
                        self.current_frame = 0
                        self.time_since_last_frame = 0

            self.handle_player_input(dt)
            self.update_animation(dt)
            self.update_screen()

    def handle_player_input(self, dt):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.player_pos.y -= self.player_speed * dt
        if keys[pygame.K_s]:
            self.player_pos.y += self.player_speed * dt
        if keys[pygame.K_q]:
            self.player_pos.x -= self.player_speed * dt
        if keys[pygame.K_d]:
            self.player_pos.x += self.player_speed * dt
        self.constrain_player()
    
    def update_animation(self, dt):
      self.time_since_last_frame += dt
      if self.current_sprite == 'ki' and self.ki_active:
          # ki 
          if self.time_since_last_frame >= self.animation_speed:
            
              self.current_frame = (self.current_frame + 1)
              
              if self.current_frame > 2:
                  self.current_frame = 1  
              self.time_since_last_frame = 0
      elif self.current_sprite == 'kame' and self.kame_active:
          # kame animation slow
          if self.time_since_last_frame >= self.kame_animation_speed:
              self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_sprite])
              self.time_since_last_frame = 0
              if self.current_frame == 0:  
                  self.kame_active = False
                  self.kame_sound.stop()
                  self.current_sprite = 'default'
      else:
          
          if self.time_since_last_frame >= self.animation_speed:
              self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_sprite])
              self.time_since_last_frame = 0

    def update_screen(self):
        
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        
        current_sprite_image = self.sprites[self.current_sprite][self.current_frame]
        if current_sprite_image:
            sprite_rect = current_sprite_image.get_rect(center=(int(self.player_pos.x), int(self.player_pos.y)))
            self.screen.blit(current_sprite_image, sprite_rect)

        pygame.display.flip()

    def constrain_player(self):
        # border
        sprite_width = self.sprites[self.current_sprite][self.current_frame].get_width()
        sprite_height = self.sprites[self.current_sprite][self.current_frame].get_height()

        if self.player_pos.x - sprite_width / 2 < 0:
            self.player_pos.x = sprite_width / 2
        if self.player_pos.x + sprite_width / 2 > self.screen_size[0]:
            self.player_pos.x = self.screen_size[0] - sprite_width / 2
        if self.player_pos.y - sprite_height / 2 < 0:
            self.player_pos.y = sprite_height / 2
        if self.player_pos.y + sprite_height / 2 > self.screen_size[1]:
            self.player_pos.y = self.screen_size[1] - sprite_height / 2


