from pygame import *
from random import randint 
from time import time as timer
import math

lost_ufos_count = 0
been_shot = 0
lifes =  3

bullets_count = 5
reload_in_progress = False
start_time = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, size_x, size_y, \
            player_x, player_y):
        super().__init__()

        self.image = transform.scale(image.load(player_image), \
            (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    
class Player(GameSprite):
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < win_height-self.size_y:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 3:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width-self.size_x:
            self.rect.x += self.speed

    def fire(self):
        global bullets_count
        global reload_in_progress
        if bullets_count > 0 and not(reload_in_progress):
            bullet_x = player.rect.centerx - 2
            bullet_y = player.rect.top - 5
            bullet = Bullet('bullet.png', 5, 5, 20, bullet_x, bullet_y)
            bullets.add(bullet)
            fire_sound.play()
            bullets_count -= 1
        elif bullets_count <= 0:
            reload_in_progress = True

def reload_ship(reloadd, s_time):
    if reloadd:
        if timer() - s_time >= 1:
            global reload_in_progress
            global bullets_count 
            bullets_count = 5
            reload_in_progress = False
            global start_time 
            start_time = 0



class Enemy(GameSprite):       
    def __init__(self, player_image, player_speed, size_x, size_y, player_x, player_y, is_countable):
        super().__init__(player_image, player_speed, size_x, size_y, player_x, player_y)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        
        self.speed = player_speed
        self.size_y = size_y
        self.size_x = size_x
        self.is_countable = is_countable
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def update(self):    
        window.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.y < win_height+self.size_y:
            self.rect.y += self.speed
        else:
            if self.is_countable:
                global lost_ufos_count
                lost_ufos_count += 1
                self.kill()
 


class Bullet(GameSprite):
    def __init__(self, player_image, player_speed, size_x, size_y, player_x, player_y):
        super().__init__(player_image, player_speed, size_x, size_y, player_x, player_y)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.size_x = size_x
        self.size_y = size_y
        self.rect.x = player_x
        self.rect.y = player_y

        mouse_x, mouse_y = mouse.get_pos()
        self.angle = math.atan2(mouse_y - player_y, mouse_x - player_x)

    def update(self):
        self.rect.x += round(self.speed * math.cos(self.angle))
        self.rect.y += round(self.speed * math.sin(self.angle))

        if self.rect.x > win_width + 50 or self.rect.x < - 50:
            self.kill()
        if self.rect.y > win_height + 50 or self.rect.y < -50:
            self.kill()


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
label_font = font.SysFont("Arial", 40)
big_font = font.SysFont("Arial", 70)

loss = big_font.render(f"Unluck... U have just lost", True, (255, 255, 255))
win = big_font.render(f"Well done. GGS mate", True, (255, 255, 255))

win_width = 1000    
win_height = 700

window = display.set_mode((win_width, win_height))
display.set_caption("Space shooter")

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

run = True
clock = time.Clock()
FPS = 60
finish = False

player = Player('rocket.png', 10, 80, 100, 300, 400)

ufos = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

asteroids_count = 3
ufos_count = 5

size_x = 80
size_y = 50
enemy_y = 0


for i in range(ufos_count):
    speed = randint(1,3)
    ufo_x = randint(0, win_width-size_x)
    ufo = Enemy('ufo.png', speed, size_x, size_y, ufo_x, enemy_y, True)
    ufos.add(ufo)

for i in range(asteroids_count):
    speed = randint(1,5)
    asteroid_x = randint(0, win_width-size_x)
    asteroid = Enemy('asteroid.png', speed, size_x, size_y, asteroid_x, enemy_y, False)
    asteroids.add(asteroid)

def increase_counter(num):
    global been_shot
    been_shot += num

def lose_a_life(num):
    global lifes 
    lifes -= num

def reboot():
    global finish 
    global lost_ufos_count
    global been_shot
    global lifes
    lost_ufos_count = 0
    been_shot = 0
    lifes =  3
    finish = False
  
    for ufo in ufos:
        ufo.kill()
    for asteroid in asteroids:
        asteroid.kill()
    






while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        if e.type == MOUSEBUTTONDOWN:
            player.fire()

        if e.type == KEYDOWN and e.key == K_r and finish == True:
            reboot()
       
        
            

   
            
    if not finish:
        window.blit(background, (0, 0))


        if lost_ufos_count >= 3:
            window.blit(loss, (200, 200))
            finish = True

        if been_shot >= 10:
            window.blit(win, (200, 200))
            finish = True


        # for ufo in ufos:
        #     if sprite.collide_rect(player, ufo):
        #         finish = True 

        for asteroid in asteroids:
            if sprite.collide_rect(player, asteroid):
                asteroid.kill()
                lose_a_life(1)
            
        if lifes <= 0:
            window.blit(loss, (200, 200))
            finish = True

        if reload_in_progress:
            if start_time == 0:
                start_time = timer()
            reload_ship(reload_in_progress, start_time)

  
        sprites_list = sprite.groupcollide(
            ufos, bullets, True, True
        )

        if sprites_list:
            increase_counter(len(sprites_list))

        


        passed = label_font.render(f"Passed: {lost_ufos_count}", True, (255, 255, 255))
        score = label_font.render(f'Score: {been_shot}', True, (255, 255, 255))
        lifes_count = label_font.render(f'lifes: {lifes}', True, (255, 255, 255))

        window.blit(passed, (30, 70))
        window.blit(score, (30, 30))
        window.blit(lifes_count, (30, 110))
        player.update()

        if len(ufos) < ufos_count:
            ufo_speed = randint(1,3)
            ufo_x = randint(0, win_width-size_x)
            ufo = Enemy('ufo.png', ufo_speed, size_x, size_y, ufo_x, enemy_y, True)
            ufos.add(ufo)

        if len(asteroids) < asteroids_count:
            asteroid_speed = randint(1,5)
            asteroid_x = randint(0, win_width-size_x)
            asteroid = Enemy('asteroid.png', asteroid_speed, size_x, size_y, asteroid_x, enemy_y, False)
            asteroids.add(asteroid)
        
        asteroids.update()
        ufos.update()
        bullets.update()
        bullets.draw(window)

        
        display.update()
        clock.tick(FPS)

