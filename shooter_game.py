from pygame import *
from random import *
from time import time as timer

mixer.init()
kick = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('WIN!', True, (255, 0, 255))
lose = font1.render('LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 30)
font3 = font.SysFont('Arial', 36)
font4 = font.SysFont('Arial', 30)
end = font4.render('Чтобы перезапустить игру нажмите Alt + f4 и включи игру', 1, (255, 255, 255))

finish = False
rek_time = False
num_fire = 30
Score = 0 #сбито
goal = 20
lost = 0 #пропущено
max_lose = 10 #макс пропусков
life = 3

win_x = 700
win_y = 500
window = display.set_mode((win_x, win_y))
display.set_caption('Шутер v2.0')
backgrout = transform.scale(
    image.load('galaxy.jpg'),
    (win_x, win_y)
)

class Player (sprite.Sprite):
    def __init__(self, p_image, x, y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fire(self):
        pass

#пуля  
class Bullet(Player):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill

#корабль
class rocket(Player):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x, 420, 15, 15, 17)
        bullets.add(bullet)

#нло
class zalupa(Player):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_y:
            self.rect.x = randint(80, win_x - 80)
            self.rect.y = 0
            lost = lost + 1

class zalupa2(Player):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_y:
            self.rect.x = randint(80, win_x - 80)
            self.rect.y = 0

Rocket = rocket('rocket.png', 25, 420, 5, 50, 60)
zlo = sprite.Group()
for i in range(1, 5):
    zlos = zalupa('ufo.png', randint(5, 660), 0, randint(1, 4), 60, 50)
    zlo.add(zlos)
zlo2 = sprite.Group()
for i in range(1, 4):
    zlos2 = zalupa2('asteroid.png', randint(5, 660), 0, randint(1, 7), 50, 50)
    zlo2.add(zlos2)
bullets = sprite.Group()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                kick.play()
                num_fire = num_fire - 1
                Rocket.fire()

    if not finish:
        FPS = 60
        clock = time.Clock()
        clock.tick(FPS)
        window.blit(backgrout,(0,0))
        lifes = font3.render('Жизней: ' +str(life),1 ,(0, 255, 0))
        window.blit(lifes, (550, 0))
        text = font2.render("Снайпнуто в палёте: " +str(Score), 1,(255, 255, 255))
        window.blit(text, (10, 5))
        lose_text = font2.render("Пропущено: " +str(lost), 1,(255, 255, 255))
        window.blit(lose_text, (10, 30))
        ammo_text = font2.render("Патронов: " +str(num_fire), 1,(255, 255, 255))
        window.blit(ammo_text, (10, 55))

        Rocket.update()
        zlo.update()
        zlo2.update()
        bullets.update()

        Rocket.reset()
        zlo.draw(window)
        zlo2.draw(window)
        bullets.draw(window)

        #пуля + объекты
        collides =  sprite.groupcollide(zlo, bullets, True, True)
        for c in collides:
            Score = Score + 1
            zlos = zalupa('ufo.png', randint(5, 660), 0, randint(1, 4), 60, 50)
            zlo.add(zlos)
        collides =  sprite.groupcollide(zlo2, bullets, False, True)
        for c in collides:
            zlos2 = zalupa2('asteroid.png', randint(5, 660), 0, randint(1, 7), 50, 50)

        coll =  sprite.spritecollide(Rocket, zlo, True)
        for c in coll:
            life = life - 1
            Score = Score + 1
            zlos = zalupa('ufo.png', randint(5, 660), 0, randint(1, 4), 60, 50)
            zlo.add(zlos)
        coll =  sprite.spritecollide(Rocket, zlo2, True)
        for c in coll:
            life = life - 1
            zlos2 = zalupa2('asteroid.png', randint(5, 660), 0, randint(1, 7), 50, 50)
            zlo2.add(zlos2)

        if Score >= goal:
            window.blit(win, (225, 225))
            window.blit(end, (25, 325))
            finish = True
        if lost >= max_lose:
            window.blit(lose, (225, 225))
            window.blit(end, (25, 325))
            finish = True
        if life <= 0:
            window.blit(lose, (225, 225))
            window.blit(end, (25, 325))
            finish = True
        if num_fire <= 0:
            window.blit(lose, (225, 225))
            window.blit(end, (25, 325))
        display.update()
