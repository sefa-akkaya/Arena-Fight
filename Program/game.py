
import pygame
from pygame import mixer
from os import walk
from time import perf_counter
from button import Button
from os.path import abspath
from os.path import dirname

mixer.init()    
pygame.init()

others_path = str(dirname(dirname(abspath(__file__)))).replace("\\", "/") + "/Others/"

WIDTH, HEIGHT = 1920,1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface1 = pygame.surface.Surface((1920, 1080))
clock = pygame.time.Clock()


# DO NOT MAKE MORE THAN 4
sound_multiplier = 3

game_music = mixer.music.load(others_path+"game_sound/game_soundtrack.mp3")
pygame.mixer.music.set_volume(0.01 * sound_multiplier)

menu_music = mixer.Sound(others_path+"game_sound/menu_music.mp3")
menu_music.set_volume(0.04 * sound_multiplier)

ninja_sword_sound = mixer.Sound(others_path+"game_sound/ninja_sword.mp3")
ninja_sword_sound.set_volume(0.04 * sound_multiplier)

knight_sword_sound = mixer.Sound(others_path+"game_sound/knight_sword.mp3")
knight_sword_sound.set_volume(0.04 * sound_multiplier)

fire_sound = mixer.Sound(others_path+"game_sound/fire_ball.mp3")
fire_sound.set_volume(0.04 * sound_multiplier)

hurt_sound = mixer.Sound(others_path+"game_sound/hurt_sound.mp3")
hurt_sound.set_volume(0.04 * sound_multiplier)

jump_sound = mixer.Sound(others_path+"game_sound/jump.mp3")
jump_sound.set_volume(0.05 * sound_multiplier)



class Player(pygame.sprite.Sprite):
    
    def __init__(self,path,x,y,facing,key,damage_frame,screen):
        super(Player,self).__init__()

        self.path_start = others_path+"PNG"
        self.attack_animation_speed = 0.25
        self.screen = screen
        self.damage_frame = damage_frame
        self.keyboard1 = key
        self.path = path
        self.path_image = self.path_start +"/" + self.path
        self.current_zort = self.default_zort  ='idle'
        self.last_zort = self.default_zort ="idle"
        self.import_char_asset()
        self.ground = self.original_ground= y
        self.rboundry = 1920
        self.frame_index = 0
        self.animation_speed = 0.25
        self.x = self.default_x = x
        self.y = self.default_y = y
        self.hitbox_width = 70
        self.hitbox_height = self.default_hitbox_height = 130
        self.hitbox = (self.x + 220, self.y+120, self.hitbox_width,self.hitbox_height)
        self.image = pygame.image.load(self.path_image+
            " PNG/idle/idle_01.png").convert()
        self.rect = self.image.get_rect(midbottom=(self.x, self.ground))
        self.image.set_colorkey((0, 0, 0))
        self.position = self.default_position = pygame.math.Vector2(self.x, self.y)
        self.velocity = self.default_velocity = pygame.math.Vector2(0,0)
        self.gravity = 0.98
        self.acceleration = self.default_acceleration = pygame.math.Vector2(0, self.gravity)
        self.acceleration_value = self.default_ac_value = 0.45
        self.friction = self.default_friction = -0.1
        self.facing = self.original_facing = facing
        self.on_ground = self.default_on_ground = True
        self.hit_rect = pygame.draw.rect(screen,(0,0,0),self.hitbox,1)
        self.hurted = self.default_hurted = False
        self.on_cooldown = self.default_on_cooldown = False
        self.cooldown_start = -5
        self.cooldown = 1.5
        self.jump_location = None
        self.health = self.default_health = 3
        self.kelle= pygame.image.load(self.path_image +" PNG/head/Head.png").convert_alpha()
        self.health_dic = {1:pygame.image.load(others_path+"PNG/galp/bir_galp.png").convert_alpha(),
                           2:pygame.image.load(others_path+"PNG/galp/iki_galp.png").convert_alpha(),
                           3:pygame.image.load(others_path+"PNG/galp/uc_galp.png").convert_alpha()}
        self.ready_image = pygame.image.load(self.path_image +" PNG/ready.png").convert_alpha()
        self.crouch_value = 0
        self.customize()
        
    def draw(self):

        if self.original_facing:
            if not self.on_cooldown:
                self.screen.blit(self.ready_image,(30,230))

            self.screen.blit(self.kelle,(-40,70))
            if self.health > 0:
                self.screen.blit(self.health_dic[self.health],(120,150))
        else:
            if not self.on_cooldown:
                self.reverse_ready_image = pygame.transform.flip(self.ready_image, True, False)
                self.screen.blit(self.reverse_ready_image,(1750,230))
            self.ters_kelle = pygame.transform.flip(self.kelle, True, False)
            self.screen.blit(self.ters_kelle,(1750,70))
            if self.health > 0:
                if self.health == 1:
                    self.screen.blit(self.health_dic[self.health],(1740,150))
                elif self.health == 2:
                    self.screen.blit(self.health_dic[self.health],(1675,150))
                elif self.health == 3:
                    self.screen.blit(self.health_dic[self.health],(1610,150))
                    
    def draw_hitbox(self):
        if self.current_zort == "crouch":
            self.crouch_value = -30
            self.hitbox_height = self.default_hitbox_height + self.crouch_value
        else:
            self.crouch_value = 0
            self.hitbox_height = self.default_hitbox_height
        self.hitbox = (self.rect.x+220,self.rect.y+120 - self.crouch_value,self.hitbox_width, self.hitbox_height)
        self.hit_rect = pygame.draw.rect(self.screen,(0,0,0),self.hitbox,1)

    def animate(self):

        if self.current_zort != self.last_zort:
            self.frame_index = 0
            self.last_zort = self.current_zort
        animation = self.animations[self.current_zort]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.current_zort]):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        if self.facing:
            self.image = self.image
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            self.image = flipped_image

    def import_image(self, path):
        surface_list = []
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def import_char_asset(self):
        char_path = self.path_image + ' PNG/'
        self.animations = {'jump': [], 'walk': [], 'idle': [], 'attack': [], 'hurt':[], 'Fireball': [], 'dead': [], "crouch":[]}

        for animation in self.animations.keys():
            full_path = char_path + animation
            self.animations[animation] = self.import_image(full_path)

    def apply_gravity(self, dt):

        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 12:
            self.velocity.y = 12
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        if self.position.y >= self.ground:
            if not self.on_ground:
                self.velocity.x *= 0.6
            self.on_ground = True
            self.velocity.y = 0
            self.position.y = self.ground
        self.rect.bottom = self.position.y

    def movement(self, dt):

        self.cooldown_finish = perf_counter()
        if self.cooldown_finish - self.cooldown_start >= self.cooldown:
            self.on_cooldown = False

        if self.hurted:        
            self.current_zort, self.last_zort = "hurt", self.current_zort
            self.animate()
            if self.frame_index >= 2:
                self.hurted = False
                self.health = self.health -1
                
            return None

        self.keys = pygame.key.get_pressed()

        self.acceleration.x = 0

        if not (self.keys[self.keyboard1["jump"]] or (self.keys[self.keyboard1["attack"]] and not self.on_cooldown)
                or self.keys[self.keyboard1["left"]] or self.keys[self.keyboard1["right"]] or 
                self.keys[self.keyboard1["crouch"]] or self.hurted or self.health <= 0):
            
            self.current_zort, self.last_zort = 'idle', self.current_zort
            self.animation_speed = 0.15
            self.animate()

        if self.hurted:        
            self.current_zort, self.last_zort = "hurt", self.current_zort
            self.animate()

        if self.keys[self.keyboard1["jump"]] and self.rect.bottom >= self.ground:
            if self.on_ground:
                pygame.mixer.Sound.play(jump_sound)

                self.current_zort, self.last_zort = 'jump', self.current_zort
                self.animation_speed = 0.25

                self.jump_location = self.hit_rect.bottomleft

                self.is_jumping = True
                self.velocity.y -= 19
                self.on_ground = False

                self.animate()

        if not self.on_cooldown and self.keys[self.keyboard1["attack"]]:
            if self.frame_index == 1 and self.last_zort == "attack" and self.path == "Knight":
                pygame.mixer.Sound.play(knight_sword_sound)
            elif self.frame_index == 1 and self.last_zort == "attack" and self.path == "Ninja":
                pygame.mixer.Sound.play(ninja_sword_sound)

            self.attack_location = self.hit_rect.center
            if self.frame_index == self.damage_frame and self.last_zort == "attack":
                self.cooldown_start = perf_counter()
                self.on_cooldown = True

            self.current_zort, self.last_zort = "attack", self.current_zort
            self.animation_speed = self.attack_animation_speed
            self.animate()
            if self.facing and self.frame_index == self.damage_frame:
                return pygame.rect.Rect(self.hit_rect.x + self.hitbox_width, self.hit_rect.y + 15, 135, 80)
            elif not self.facing and self.frame_index == self.damage_frame:
                return pygame.rect.Rect(self.hit_rect.x - 135, self.hit_rect.y + 5, 140, 80)


        elif self.keys[self.keyboard1["left"]]:
            self.image = pygame.transform.rotate(self.image, 180)
            self.acceleration.x -= self.acceleration_value
            self.current_zort, self.last_zort = "walk", self.current_zort
            if (self.hitbox[0] < 0):
                self.position.x = -220
                self.velocity.x = 0
            self.facing = False
            self.animation_speed = 0.25
            self.animate()

        elif self.keys[self.keyboard1["right"]]:
            self.acceleration.x += self.acceleration_value
            self.current_zort, self.last_zort = "walk", self.current_zort
            if (self.hit_rect.right >= self.rboundry):
                self.position.x = (self.rboundry - self.rect.width / 2) - self.hitbox_width / 2
                self.velocity.x = 0
            self.animation_speed = 0.25
            self.facing = True
            self.animate()

        elif self.keys[self.keyboard1["crouch"]]:
            self.current_zort, self.last_zort = "crouch", self.current_zort
            self.hitbox_width, self.hitbox_height
            self.animate()

        if self.on_ground:
            self.acceleration.x += self.velocity.x * self.friction
        else:
            self.acceleration.x += self.velocity.x * self.friction * 0.4

        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity()
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt*dt)
        self.rect.x = self.position.x

    def limit_velocity(self):
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def restart(self):

        self.current_zort = self.default_zort
        self.last_zort = self.default_zort
        self.import_char_asset()
        self.ground = self.original_ground
        self.x = self.default_x
        self.y = self.default_y
        self.hitbox_width = 70
        self.hitbox_height = 130
        self.hitbox = (self.x + 220, self.y+120, self.hitbox_width,self.hitbox_height)
        self.image.set_colorkey((0, 0, 0))
        self.position = pygame.math.Vector2(self.default_x, self.default_y)
        self.velocity = self.default_velocity
        self.acceleration = self.default_acceleration
        self.acceleration_value = self.default_ac_value
        self.friction = self.default_friction
        self.facing = self.original_facing
        self.on_ground = self.default_on_ground
        self.hurted = self.default_hurted
        self.on_cooldown = self.default_on_cooldown
        self.health = self.default_health

    def customize(self):
        if self.path == "Dragon":
            self.cooldown = 2.5
        elif self.path == "Ninja":
            self.default_ac_value = 0.65
            self.acceleration_value = 0.65
            self.cooldown = 1

    def update(self, dt):
        if self.health <= 0:
            self.current_zort, self.last_zort = "dead", self.current_zort
            self.animate()
            self.apply_gravity(dt)
            return None
        a = self.movement(dt)
        self.apply_gravity(dt)
        self.draw()
        if a:
            return a


class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, sound):
        super().__init__()

        self.sound = sound
        self.screen = screen
        self.is_finished = False
        self.path =others_path+ "PNG/particles"
        self.import_char_asset()
        self.fire_hit_rect = None
        self.fire_x, self.fire_y = 0, 0
        self.fire_hitbox_width, self.fire_hitbox_height = 70,40
        self.fire_hitbox = (self.fire_x, self.fire_y, self.fire_hitbox_width,self.fire_hitbox_height)
        self.edge = (0,0,0,0)
        self.frame_index = 0
        self.animation_speed = 0.25
        self.fire_finish = False
        self.fire_gone = False
        self.fire_image = None
    
    def animate(self):

        animation = self.animations['fireball']
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(self.animations['fireball']):
            self.frame_index = 0
            self.is_finished = True

        self.fire_image = animation[int(self.frame_index)]
        if self.fire_facing:
            self.fire_image = self.fire_image
        else:
            flipped_image = pygame.transform.flip(self.fire_image, True, False)
            self.fire_image = flipped_image

    def import_image(self, path):

        surface_list = []
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def import_char_asset(self):

        self.animations = {'jumpeffect': [], 'fireball':[]}

        for animation in self.animations.keys():
            full_path = self.path + '/' + animation
            self.animations[animation] = self.import_image(full_path)
    
    def fire_ball_movement(self):

        if self.fire_gone:
            if self.fire_facing:
                if self.fire_x <= 2000:
                    self.fire_x += 13
            else:
                if self.fire_x >= -200:
                    self.fire_x -= 13
    
    def fire_breath(self, player):

        if player.path == "Dragon":
            if player.keys[player.keyboard1["attack"]] and player.on_cooldown and player.last_zort == "attack":
                if not self.fire_gone:
                    pygame.mixer.Sound.play(fire_sound)
                    self.fire_facing = player.facing
                    self.fire_gone = True
                    self.fire_x, self.fire_y = player.attack_location
                    self.fire_y -= 25

        if self.fire_gone:
            self.fire_finish = False
            self.animate()

    def fire_hitbox_draw(self):

        if self.fire_finish:
            # Hitbox uzağa ışınlanır.
            self.fire_hitbox = (0, 0, self.fire_hitbox_width,self.fire_hitbox_height)
            self.fire_hit_rect = pygame.draw.rect(self.screen,(0,0,0),self.fire_hitbox,1)
            self.edge = (0,0)

        else:
            # Hitbox normal şekilde çizilir.
            self.fire_hitbox = (self.fire_x, self.fire_y, self.fire_hitbox_width,self.fire_hitbox_height)
            self.fire_hit_rect = pygame.draw.rect(self.screen,(0,0,0),self.fire_hitbox,1)
    
    def draw(self): 
            
        if self.fire_gone:

            self.edge = pygame.rect.Rect(self.fire_x, self.fire_y, self.fire_hitbox_width,self.fire_hitbox_height)

            self.screen.blit(self.fire_image, (self.fire_x, self.fire_y))

    def update(self,player):
        
        self.fire_breath(player)
        self.fire_ball_movement()
        self.draw()


class Particles:

    def __init__(self, screen):

        self.screen = screen
        self.fire_facing = True
        self.path =others_path+ "PNG/particles"
        self.import_char_asset()
        self.image = None
        self.facing = True
        self.frame_index = 0
        self.x, self.y = None, None
        self.animation_speed = 0.35

    def animate(self):

        animation = self.animations['jumpeffect']
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(self.animations['jumpeffect']):
            self.frame_index = 0
            self.is_finished = True

        
        self.image = animation[int(self.frame_index)]
        if self.facing:
            self.image = self.image
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            self.image = flipped_image
        if self.is_finished:
            self.image = None
            return None

    def import_image(self, path):

        surface_list = []
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def import_char_asset(self):

        self.animations = {'jumpeffect': [], 'fireball':[]}

        for animation in self.animations.keys():
            full_path = self.path + '/' + animation
            self.animations[animation] = self.import_image(full_path)
        
    def jump(self, player):

        if not player.on_ground and not self.is_finished:
            self.facing = player.facing 
            self.x , self.y = player.jump_location
            self.animate()

    def draw(self, screen):
        
        if self.image:
            if self.facing:
                screen.blit(self.image, (self.x - 100, self.y-50))
            else:
                screen.blit(self.image, (self.x + 20, self.y-50))
        
    def update(self, screen, player):

        self.jump(player)
        self.draw(screen)

        if player.on_ground:
            self.is_finished = False
        
     
class Collision():

    def __init__(self):
        pass

    def collide(self, player_a, player_b):

        if player_a.hit_rect.colliderect(player_b.hit_rect):
            
            if(player_a.hit_rect.bottom > player_b.hit_rect.top  and player_a.hit_rect.bottom < player_b.hit_rect.top + 50):
                player_a.ground =  player_b.position.y - player_b.hitbox_height
            if(player_b.hit_rect.bottom > player_a.hit_rect.top  and player_b.hit_rect.bottom < player_a.hit_rect.top + 50):
                player_b.ground =  player_a.position.y - player_a.hitbox_height
                
                
            if player_a.ground == player_b.position.y - player_b.hitbox_height or  player_b.ground == player_a.position.y - player_a.hitbox_height :
                player_a.friction = -0.1
                player_b.friction = -0.1
                player_a.acceleration_value = player_a.default_ac_value
                player_b.acceleration_value = player_b.default_ac_value
            else:
                player_a.friction = -2
                player_a.acceleration_value *=-1
                player_b.friction = -2
                player_b.acceleration_value *=-1
            

        else:
            player_a.ground = player_a.original_ground
            player_b.ground = player_b.original_ground
            player_a.friction = -0.1
            player_b.friction = -0.1
            player_a.acceleration_value = player_a.default_ac_value
            player_b.acceleration_value = player_b.default_ac_value
             
    def hit(self, player_a, player_b, hit_point_a, hit_point_b):

        if player_a.path != "Dragon":
            if hit_point_a:
                if player_b.hit_rect.colliderect(hit_point_a):
                    if player_b.path == "Knight" and player_b.on_cooldown == False and player_b.keys[player_b.keyboard1["attack"]] and player_a.path != "Knight":
                        player_b.on_cooldown = True
                        player_b.cooldown_start = perf_counter()
                    elif player_b.hurted == False:
                        player_b.hurted = True
                        pygame.mixer.Sound.play(hurt_sound)

        if player_b.path != "Dragon":
            if hit_point_b:
                if player_a.hit_rect.colliderect(hit_point_b):
                    if player_a.path == "Knight" and player_a.on_cooldown == False and player_a.keys[player_a.keyboard1["attack"]] and player_b.path != "Knight":
                        player_a.on_cooldown = True
                        player_a.cooldown_start = perf_counter()
                    elif player_a.hurted == False:    
                        player_a.hurted = True
                        pygame.mixer.Sound.play(hurt_sound)

    def burn(self, player_a, hit_point_a, fire, screen):

        if player_a.path == "Knight":
            if hit_point_a:
                if hit_point_a.colliderect(fire.fire_hitbox):
                    fire.fire_finish = True
                    fire.fire_gone = False

        if player_a.hit_rect.colliderect(fire.fire_hitbox):
            if player_a.path == "Knight" and player_a.on_cooldown == False and player_a.keys[player_a.keyboard1["attack"]]:
                fire.fire_finish = True
                fire.fire_gone = False
                player_a.on_cooldown = True
                player_a.cooldown_start = perf_counter()
            else: 
                if player_a.hurted == False:
                    player_a.hurted = True
                    pygame.mixer.Sound.play(hurt_sound)
                    fire.fire_finish = True
                    fire.fire_gone = False
            
        if (fire.edge[0] >= screen.get_width()+50) or (fire.edge[0] <= -50):
            fire.fire_finish = True
            fire.fire_gone = False



key1 = {"jump":pygame.K_w, "attack": pygame.K_SPACE, "right": pygame.K_d, "left": pygame.K_a, "crouch": pygame.K_s}
key2 = {"jump":pygame.K_KP_8, "attack": pygame.K_RCTRL, "right": pygame.K_KP_6, "left": pygame.K_KP_4, "crouch": pygame.K_KP_5}

game_active = False
character_select = False
restart_menu = False
selection = 2

bg = pygame.image.load(others_path+"PNG/backgroundpng/arena.png").convert()
menu = pygame.image.load(others_path+"PNG/backgroundpng/menu.png").convert()
selection_menu = pygame.image.load(others_path+"PNG/backgroundpng/selection.png").convert()
pointer = pygame.image.load(others_path+"PNG/backgroundpng/pointer.png").convert_alpha()

Knight1 = Player("Knight",300,800,True,key1,5,screen)
Knight2 = Player("Knight",900,800,False,key2,5,screen)
Dragon1 = Player("Dragon",300,800,True,key1,2,screen)
Dragon2 = Player("Dragon",900,800,False,key2,2,screen)
Ninja1 = Player("Ninja",300,800,True,key1,5,screen)
Ninja2 = Player("Ninja",900,800,False,key2,5,screen)

font = pygame.font.Font(others_path+"Font/DRAGON HUNTER 400.otf", 90)

player1_text = font.render("Player 1 is selecting", 1, (20,20,20))
player2_text = font.render("Player 2 is selecting", 1, (20,20,20))

particle1 = Particles(screen)
particle2 = Particles(screen)

bullet1 = Bullet(screen, fire_sound)
bullet2 = Bullet(screen, fire_sound)

TARGET_FPS = 60

hitbox = pygame.Rect(0,0,100,100)
collider = Collision()

play_menu_music = True

pause = False

sound_on = True

play_button = Button(image=pygame.image.load(others_path+"PNG/buttons/play.png").convert_alpha(), 
                             image_click=pygame.image.load(others_path+"PNG/buttons/play_click.png").convert_alpha(),
                              pos=(WIDTH/2, HEIGHT/2 - 50))

volume_on_button = Button(image=pygame.image.load(others_path+"PNG/buttons/volume_on.png").convert_alpha(), 
                                image_click=pygame.image.load(others_path+"PNG/buttons/volume_on_click.png").convert_alpha(),
                                pos=((WIDTH/18)*17 - 20, (HEIGHT/18)*2))

volume_off_button = Button(image=pygame.image.load(others_path+"PNG/buttons/volume_off.png").convert_alpha(), 
                            image_click=pygame.image.load(others_path+"PNG/buttons/volume_off_click.png").convert_alpha(),
                            pos=((WIDTH/18)*17 - 20, (HEIGHT/18)*2))

ninja_button = Button(image=pygame.image.load(others_path+"PNG/buttons/ninja_select.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/ninja_selected.png").convert_alpha(),
                        pos=((WIDTH/2), HEIGHT/2))

knight_button = Button(image=pygame.image.load(others_path+"PNG/buttons/knight_select.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/knight_selected.png").convert_alpha(),
                        pos=((WIDTH/18)*3, HEIGHT/2))

dragon_button = Button(image=pygame.image.load(others_path+"PNG/buttons/dragon_select.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/dragon_selected.png").convert_alpha(),
                        pos=((WIDTH/18)*15, HEIGHT/2))

restart_button = Button(image=pygame.image.load(others_path+"PNG/buttons/refresh_button.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/refresh_button_click.png").convert_alpha(),
                        pos=(WIDTH/3, HEIGHT/2 ))

continue_button = Button(image=pygame.image.load(others_path+"PNG/buttons/continue_button.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/continue_button_click.png").convert_alpha(),
                        pos=(WIDTH/2, HEIGHT/2 - 50))

quit_button = Button(image=pygame.image.load(others_path+"PNG/buttons/quit.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/quit_click.png").convert_alpha(),
                        pos=(WIDTH/2, HEIGHT/2 + 150))

while True:
    dt = clock.tick(60) * .001 * TARGET_FPS
    
    if (not game_active):
        if play_menu_music and sound_on:
            pygame.mixer.Sound.play(menu_music)
            play_menu_music = False

    if (not game_active) and (not character_select):

        screen.blit(menu,(0,0))
        menu_mouse_pos = pygame.mouse.get_pos()

        play_button.changeColor(menu_mouse_pos, True)
        play_button.update(screen)

        quit_button.changeColor(menu_mouse_pos, True)
        quit_button.update(screen)

        if sound_on:
            volume_on_button.changeColor(menu_mouse_pos, False)
            volume_on_button.update(screen)
        else:
            volume_off_button.changeColor(menu_mouse_pos, False)
            volume_off_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_on:
                    if volume_on_button.checkForInput(menu_mouse_pos, False):
                        sound_on = False
                        pygame.mixer.pause()
                else:
                    if volume_off_button.checkForInput(menu_mouse_pos, False):
                        sound_on = True
                        pygame.mixer.unpause()
                
                if quit_button.checkForInput(menu_mouse_pos, True):
                    pygame.quit()
                    exit()

                if play_button.checkForInput(menu_mouse_pos, True):
                    character_select = True
                    break

    if character_select:

        quit_button = Button(image=pygame.image.load(others_path+"PNG/buttons/quit.png").convert_alpha(), 
                        image_click=pygame.image.load(others_path+"PNG/buttons/quit_click.png").convert_alpha(),
                        pos=(WIDTH/2, HEIGHT/2 + 150))

        screen.blit(selection_menu,(0,0))
        if selection == 2:
             screen.blit(player1_text, (WIDTH // 2 - player1_text.get_width() //
                         2, HEIGHT // 3 - player1_text.get_height()))
        elif selection == 1:
            screen.blit(player2_text, (WIDTH // 2 - player2_text.get_width() //
                         2, HEIGHT // 3 - player2_text.get_height()))

        menu_mouse_pos = pygame.mouse.get_pos()

        if pause:

            continue_button.update(screen)
            continue_button.changeColor(menu_mouse_pos, True)
            quit_button.changeColor(menu_mouse_pos, True)
            quit_button.update(screen)

            if sound_on:
                volume_on_button.changeColor(menu_mouse_pos, False)
                volume_on_button.update(screen)
            else:
                volume_off_button.changeColor(menu_mouse_pos, False)
                volume_off_button.update(screen)
            
        else:
            if ninja_button.changeColor(menu_mouse_pos, False):
                screen.blit(pointer, ((WIDTH/39)*18 + 30, HEIGHT*16/24))
            ninja_button.update(screen)


            if knight_button.changeColor(menu_mouse_pos, False):
                screen.blit(pointer, ((WIDTH/39)*6 -5, HEIGHT*16/24))
            knight_button.update(screen)


            if dragon_button.changeColor(menu_mouse_pos, False):
                screen.blit(pointer, ((WIDTH/39)*32, HEIGHT*16/24))
            dragon_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    if pause == True:
                        pause = False
                    elif pause == False:
                        pause = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause:
                    if sound_on:
                        if volume_on_button.checkForInput(menu_mouse_pos, False):
                            sound_on = False
                            pygame.mixer.pause()
                    else:
                        if volume_off_button.checkForInput(menu_mouse_pos, False):
                            sound_on = True
                            pygame.mixer.unpause()

                    if continue_button.checkForInput(menu_mouse_pos, True):
                        pause = False
                    if quit_button.checkForInput(menu_mouse_pos, True):
                        pygame.quit()
                        exit()
                else:
                    if ninja_button.checkForInput(menu_mouse_pos, False):
                        if selection == 2:
                            selection -= 1
                            player1 = Ninja1
                        else:
                            selection -= 1
                            player2 = Ninja2
                    
                    if knight_button.checkForInput(menu_mouse_pos, False):
                        if selection == 2:
                            selection -= 1
                            player1 = Knight1
                        else:
                            selection -= 1
                            player2 = Knight2

                    if dragon_button.checkForInput(menu_mouse_pos, False):
                        if selection == 2:
                            selection -= 1
                            player1 = Dragon1
                        else:
                            selection -= 1
                            player2 = Dragon2

        if selection == 0:
            game_active = True
            character_select = False

# Play Phase
    if game_active:
        if play_menu_music == False:
            play_menu_music = True
            if sound_on:
                pygame.mixer.Sound.stop(menu_music)
                pygame.mixer.music.play(loops = -1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause:
                    if sound_on:
                        if volume_on_button.checkForInput(menu_mouse_pos, False):
                            sound_on = False
                            pygame.mixer.pause()
                            pygame.mixer.music.stop()
                    else:
                        if volume_off_button.checkForInput(menu_mouse_pos, False):
                            sound_on = True
                            pygame.mixer.unpause()
                            pygame.mixer.music.play()
                    if continue_button.checkForInput(menu_mouse_pos, True):
                        pause = False
                    if quit_button.checkForInput(menu_mouse_pos, True):
                        pygame.quit()
                        exit()

                if restart_menu:

                    if sound_on:
                        if volume_on_button.checkForInput(menu_mouse_pos, False):
                            sound_on = False
                            pygame.mixer.pause()
                            pygame.mixer.music.stop()
                    else:
                        if volume_off_button.checkForInput(menu_mouse_pos, False):
                            sound_on = True
                            pygame.mixer.unpause()
                            pygame.mixer.music.play()
                            
                    if restart_button.checkForInput(menu_mouse_pos, False):
                        pygame.mixer.music.stop()
                        restart_menu = False
                        game_active = False
                        character_select = True
                        selection = 2
                        player1.restart()
                        player2.restart()

                    if quit_button.checkForInput(menu_mouse_pos, True):
                        pygame.quit()
                        exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    if pause == True:
                        pause = False
                    elif pause == False:
                        pause = True

        if not pause:
            bullet1.fire_hitbox_draw()
            bullet2.fire_hitbox_draw()
            player1.draw_hitbox()
            player2.draw_hitbox()
            screen.blit(bg,(0,0))
            collider.collide(player1, player2)
            player1_hit_rect, player2_hit_rect = player1.update(dt), player2.update(dt)
            collider.hit(player1, player2, player1_hit_rect, player2_hit_rect)
            if player1 == Dragon1:
                collider.burn(player2, player2_hit_rect, bullet1, screen)
                bullet1.update(player1)
            if player2 == Dragon2:
                collider.burn(player1, player1_hit_rect, bullet2, screen)
                bullet2.update(player2)
            particle1.update(screen, player1)
            particle2.update(screen, player2)
            if player1.health <= 0:
                restart_menu = True
                winner = "Player 2"
            elif player2.health <= 0:
                restart_menu = True
                winner = "Player 1"
            screen.blit(player1.image,(player1.rect.x,player1.rect.y))
            screen.blit(player2.image,(player2.rect.x,player2.rect.y))

        elif pause:
            screen.blit(bg,(0,0))
            screen.blit(player1.image,(player1.rect.x,player1.rect.y))
            screen.blit(player2.image,(player2.rect.x,player2.rect.y))
            menu_mouse_pos = pygame.mouse.get_pos()

            continue_button.update(screen)
            continue_button.changeColor(menu_mouse_pos, True)
            quit_button.changeColor(menu_mouse_pos, True)
            quit_button.update(screen)

            if sound_on:
                volume_on_button.changeColor(menu_mouse_pos, False)
                volume_on_button.update(screen)
            else:
                volume_off_button.changeColor(menu_mouse_pos, False)
                volume_off_button.update(screen)

        if restart_menu:
            pause = False
            menu_mouse_pos = pygame.mouse.get_pos()
            winner_text = font.render(winner + " won", 1, (20,20,20))
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() //
                        2, HEIGHT // 4 - winner_text.get_height()))
            restart_button.changeColor(menu_mouse_pos, True)
            restart_button.update(screen)

            quit_button = Button(image=pygame.image.load(others_path+"PNG/buttons/quit.png").convert_alpha(), 
                                    image_click=pygame.image.load(others_path+"PNG/buttons/quit_click.png").convert_alpha(),
                                    pos=(WIDTH*2/3, HEIGHT/2))

            quit_button.changeColor(menu_mouse_pos, True)
            quit_button.update(screen)

            if sound_on:
                volume_on_button.changeColor(menu_mouse_pos, False)
                volume_on_button.update(screen)
            else:
                volume_off_button.changeColor(menu_mouse_pos, False)
                volume_off_button.update(screen)
    pygame.display.update()
