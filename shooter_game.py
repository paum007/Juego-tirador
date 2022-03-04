from pygame import *
from random import randint
from time import time as timer


# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)
        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# clase del jugador principal
class Player(GameSprite):
    # movimiento del jugador
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

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        Bullets.add(bullet)


lost = 0

#calse del enemigo
class Enemy(GameSprite):
    #movimiento del enemigo
    def update(self):
        self.rect.y += self.speed
        global lost
        #para desaparecer cuando llege el borde de la pantalla
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#clase de la bala 
class Bullet(GameSprite):
    #movimiento de la bala
    def update(self):
        self.rect.y += self.speed
        #para desaparecer cuando llege al borde
        if self.rect.y < 0:
            self.kill()

#escena del juego:
win_width = 900
win_height = 600
window = display.set_mode((win_width, win_height))
#imágenes
img_background = "pixel spiral galaxy.png"
img_player = "Nave2.png"
img_enemy = "enemy.gif"
img_bullet = "bullet.png"
img_ast = "asteroide.png"
#sonido
snd_background = "Voxel-Revolution.ogg"
snd_bullet = "fire.ogg"

display.set_caption("Galaxy")
background = transform.scale(image.load(img_background), (win_width, win_height))


#música y efectos
mixer.init()
mixer.music.load(snd_background)
mixer.music.set_volume(0.3)
mixer.music.load(snd_background)
mixer.music.play()


score = 0
lost = 0
max_lost = 3
goal = 10


#creando fuentes
font.init()
font2 = font.SysFont('Arial', 36)

font3 = font.SysFont('Arial', 100)


lose = font3.render("Perdiste ", 1, (224, 0, 0))
win = font3.render("Ganaste ", 3, (27, 181, 30))

#jugador y objetos
player = Player(img_player, 5, win_height - 115, 105, 106, 6)

Alien = sprite.Group()
for i in range(1, 6):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(1, 2))
    Alien.add(enemy)

Bullets = sprite.Group()


asteroids = sprite.Group() 
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

num_fire = 0 
rel_time = False

#bucle para que funcione el juego
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
            #para comprobar cuantas balas he disparado
            if num_fire < 5 and rel_time == False:
                num_fire = num_fire + 1
                player.fire() 

    if num_fire  >= 5 and rel_time == False : #si el jugador hizo 5 disparos
                       last_time = timer() #registra el tiempo cuando esto sucedió
                       rel_time = True #establece la bandera de reinicio

    if not finish:
        #actualizando el fondo
        window.blit(background, (0,0))

        #creando el texto cuando pierdes
        text_lose = font2.render("Fallados: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        Bullets.draw(window)
        Alien.draw(window)
        asteroids.draw(window)
        player.reset()

        Bullets.update()
        Alien.update()
        asteroids.update()
        player.update()
        

        #comprueba la colision entre una bala y los mounstros
        collides = sprite.groupcollide(Alien, Bullets, True, True)
        for c in collides:
            #se repite tantas veces como se golpee con los enemigos
            score = score + 1
            enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(1, 2))
            Alien.add(enemy)

        #comprueba la colision entre la otra bala y los mounstros
        collides1 = sprite.groupcollide(asteroids, Bullets, True, True)
        for c in collides1:
            #se repite tantas veces como se golpee con los enemigos
            asteroid = Enemy(img_enemy, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)
        
        #derrota: entran muchos enemigos o el cohete se choca contra los enemigos
        if sprite.spritecollide(player, Alien, True) or lost >= max_lost:
            finish = True
            window.blit(lose, (320, 250))
        if score >= goal:
            finish = True
            window.blit(win, (320, 250))
        #para que se escriba el texto en la pantalla
        text = font2.render("Puntuaje: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Fallados: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        


    display.update()
    clock.tick(FPS)