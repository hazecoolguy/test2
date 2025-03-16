from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
    
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

class Player(GameSprite):
    def update(self):
        keypressed = key.get_pressed()
        if keypressed[K_LEFT] and self.rect.x > 15:
            self.rect.x -= self.speed
        if keypressed[K_RIGHT] and self.rect.x < 700-15-65:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('laserbulet.png', self.rect.centerx, self.rect.y,15,30,3)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700-self.rect.height:
            self.rect.x = randint(10, 700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,2)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

window = display.set_mode((700,700))
display.set_caption('SpaceShooter')
background = transform.scale(image.load('space.jpg'), (700,700))

mixer.init()
mixer.music.load('gamemusic.ogg')
mixer.music.play()
#! шрифты
font.init()
font1 = font.SysFont('Arial', 36)

#! спрайты
player = Player('monkey.png',300,600,100,100,5)
bullets = sprite.Group()

enemy_count = 6
enemies = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('banana.png', randint(10,700-10-70),-40, 70,40, randint(1,2))
    enemies.add(enemy)

playb = GameSprite('playb.png', 290,320,100,50,0)

game = True
finish = True
menu = True
clock = time.Clock()
FPS = 120
lost = 0
kill = 0

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if menu:
        window.blit(background, (0,0))
        playb.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if playb.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False

    if  not finish:
        window.blit(background,(0,0))

        player.update()
        player.reset()

        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        lost_enemy = font1.render('Пропущено '+str(lost),1,(255,255,255))
        kill_enemy = font1.render('Убито '+str(kill),1,(255,255,255))

        window.blit(lost_enemy, (10,10))
        window.blit(kill_enemy, (10,40))

        sprite_list = sprite.groupcollide(enemies, bullets, True, True)
        
        for i in range(len(sprite_list)):
            kill += 1
            enemy = Enemy('banana.png', randint(10,700-10-70),-40, 70,40, randint(1,2))
            enemies.add(enemy)

        if kill > 10:
            finish = True  
            ftext = font1.render('you won!', 1, (255,255,255))
            window.blit(ftext, (300,200))

        sprite_list = sprite.spritecollide(player, enemies, True)          
        if lost > 5 or len(sprite_list)>0:
            finish = True
            ltext = font1.render('you lost!', 1, (255,255,255))
            window.blit(ltext, (300,200))

    display.update()
    clock.tick(FPS)
