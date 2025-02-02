from pygame import*
from random import randint

init()

W, H = 500, 700
FPS = 60


mixer.init()
mixer.music.load("sounds/space.ogg")
mixer.music.set_volume(0.5)
mixer.music.play()

shoot_snd = mixer.Sound('sounds/fire.ogg')

font.init()
font1 = font.SysFont('fonts/Bebas_Neue_Cyrillic.ttf', 35, bold=True)
font2 = font.SysFont('fonts/Bebas_Neue_Cyrillic.ttf', 100, bold=True)


window = display.set_mode((W, H))
display.set_caption("Shooter")

bg = transform.scale(image.load('images/galaxy.jpg'), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, img):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - self.width:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 20, 20, 'images/bullet.png' )
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global skipped
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.width)
            self.rect.y = 0
            skipped += 1

class Asteroid(GameSprite):
    def __init__(self, x, y, width, height, speed, img):
        super().__init__(x, y, width, height, speed, img)
        self.angle = 0
        self.original_image = self.image
    def update(self):
        self.rect.y += self.speed
        self.angle = (self.angle + 2.5) % 360
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.width)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()       
        
player = Player(W / 2, H - 100, 50, 100, 5, 'images/rocket.png')
enemies = sprite.Group()
for i in range(6):
    enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(2, 4), 'images/ufo.png')
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(2, 4), 'images/asteroid.png')
    asteroids.add(asteroid)

bullets = sprite.Group()

life = 3
kill = 0
skipped = 0
shoot_count = 30 

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if shoot_count > 0:
                    shoot_snd.play()
                    player.shoot()
                    shoot_count -= 1

    window.blit(bg, (0, 0))
    player.draw()
    player.move()
    enemies.draw(window)
    enemies.update()

    asteroids.draw(window)
    asteroids.update()

    bullets.draw(window)
    bullets.update()
    # зіткнення куль з ворогами
    if sprite.groupcollide(bullets, enemies, True, True):
        kill += 1
        enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(2, 4), 'images/ufo.png')
        enemies.add(enemy)
    # зіткнення куль з астеройдами
    if sprite.groupcollide(bullets, asteroids, True, False):
        pass
    # зіткнення гравйця з астройдами
    if sprite.spritecollide(player, asteroids, True):
        life -= 1
        asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(2, 4), 'images/asteroid.png')
        asteroids.add(asteroid)
    # зіткнення гравця з ворогами
    if sprite.spritecollide(player, enemies, True):
        life -= 1
        enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(2, 4), 'images/ufo.png')
        enemies.add(enemy)

    if life < 0:
        game = False  

    skipped_txt = font1.render(f'Пропущено: {skipped}',True, (255, 255, 255))
    window.blit(skipped_txt, (10, 10))

    killed_txt = font1.render(f'Вбито: {kill}', True, (255, 255, 255))
    window.blit(killed_txt, (10, 40))

    life_txt = font2.render(str(life), True, (0, 255, 0))
    window.blit(life_txt, (450, 5))

     



    display.update()
    clock.tick(FPS)