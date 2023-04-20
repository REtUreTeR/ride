#Створи власний Шутер!
from pygame import *
from random import randint


mixer.init()
mixer.music.load('ret.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))

img_back = "roader.png"
bg = "roader.png"
img_hero = "arer.png"
img_bullet = "bullet.png"
img_enemy = "pol.png"

score = 0
lost= 0

goal = 10
max_lost = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
       
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
        
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 80, 60, 100, 7)

monsters = sprite.Group()
for i in range(1, 10):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -500, 80, 90, randint(1, 9))
    monsters.add(monster)
bullets = sprite.Group()

finish = False

run = True

by = 0

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    



    if not finish:
        window.blit(background, (0, by))
        window.blit(background, (0, by + 500))

        text = font2.render("Рахунок: " + str(lost), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)



        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -500, 80, 90, randint(1, 9))
            monsters.add(monster)

        
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200, 200))
        

        if lost >= max_lost:
            finish = True
            window.blit(win, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        by -= 5
        if by == -500:
            by = 0
        display.update()
    time.delay(50)
    




