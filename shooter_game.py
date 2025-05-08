from pygame import *
from random import randint
from time import time as timer


# Parent class for other objects
class GameSprite(sprite.Sprite):
    # Constructor of the class
    def __init__(self, img_player, player_x, player_y, size_x, size_y, player_speed):
        # calling the Sprite class constructor:
        sprite.Sprite.__init__(self)
        # each object stores an 'image' property
        self.image = transform.scale(image.load(img_player), (size_x, size_y))
        self.speed = player_speed
        # each object stores a 'rect' property defining its position
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # method that draws the character on the screen
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Player class
class Player(GameSprite):
    # player movement
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        Bullets.add(bullet)
        mixer.Sound(snd_bullet).play()


lost = 0

# Enemy class
class Enemy(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        # when the enemy reaches the bottom of the screen, reset its position and increment lost count
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# Bullet class
class Bullet(GameSprite):
    # bullet movement
    def update(self):
        self.rect.y += self.speed
        # to disappear when it reaches the top of the screen
        if self.rect.y < 0:
            self.kill()

# Game scene:
win_width = 900
win_height = 600
window = display.set_mode((win_width, win_height))
# images
img_background = "Images/pixel spiral galaxy.png"
img_player = "Images/Nave2.png"
img_enemy = "Images/enemy.gif"
img_bullet = "Images/bullet.png"
img_ast = "Images/asteroide.png"
# sound
snd_background = "Sounds/Voxel-Revolution.ogg"
snd_bullet = "Sounds/pewpew.ogg"

display.set_caption("Galaxy")
background = transform.scale(image.load(img_background), (win_width, win_height))


# music and effects
mixer.init()
mixer.music.load(snd_background)
mixer.music.set_volume(0.3)
mixer.music.load(snd_background)
mixer.music.play()


score = 0
lost = 0
max_lost = 3
goal = 10


# creating fonts
font.init()
# Load custom pixel font
pixel_font = font.Font("Fonts/pixel.ttf", 10)     # for normal size
pixel_font_big = font.Font("Fonts/pixel.ttf", 70)   # for big text like "Perdiste"

font2 = pixel_font
font3 = pixel_font_big

lose = font3.render("You Lose!", 1, (224, 0, 0))
win = font3.render("You Win!", 3, (27, 181, 30))

win_rect = win.get_rect(center=(win_width // 2, win_height // 2))
lose_rect = lose.get_rect(center=(win_width // 2, win_height // 2))


# player and objects
player = Player(img_player, 5, win_height - 115, 105, 106, 6)

Alien = sprite.Group()
for i in range(1, 6):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(1, 2))
    Alien.add(enemy)

Bullets = sprite.Group()


asteroids = sprite.Group() 
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

num_fire = 0 
rel_time = False

# game loop
game = True
finish = False
clock = time.Clock()
FPS = 60


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire() 

    if not finish:
        # updating the background
        window.blit(background, (0, 0))

        # creating the text for when you lose
        text_lose = font2.render("Enemies missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        Bullets.draw(window)
        Alien.draw(window)
        asteroids.draw(window)
        player.reset()

        Bullets.update()
        Alien.update()
        asteroids.update()
        player.update()
        
        # check collision between bullet and enemies
        collides = sprite.groupcollide(Alien, Bullets, True, True)
        for c in collides:
            # repeated for each enemy hit
            score = score + 1
            enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(1, 2))
            Alien.add(enemy)

        # check collision between bullet and asteroids
        collides1 = sprite.groupcollide(asteroids, Bullets, True, True)
        for c in collides1:
            asteroid = Enemy(img_enemy, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)
        
        # defeat: too many enemies have entered or the spaceship collides with an enemy
        if sprite.spritecollide(player, Alien, True) or lost >= max_lost:
            finish = True
            window.blit(lose, lose_rect)
        
        # victory: spaceship has eliminated enough enemies
        if score >= goal:
            finish = True
            window.blit(win, win_rect)
        # render text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Enemies missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

    display.update()
    clock.tick(FPS)