import pygame
import random
import math
from pygame import mixer

# Inicializamos el juego
pygame.init()

# Creamos la pantalla
# (X, Y) --> (800, 600)
screen = pygame.display.set_mode((800, 600))

# Fondo
fondo = pygame.image.load('fondo.png')#.convert()#.convert nos hace correr el juego mas rapido

# Musica de Fondo
mixer.music.load('background.wav')
# -1-->bucle
mixer.music.play(-1)

# Titulo e icono
pygame.display.set_caption("Espacio invadido")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

######Player#########
# player.png--> 64px
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
# playerX_change--> velocidad inicial
playerX_change = 0

######Invasor#########
enemyImg = []
enemyX = []
enemyY = []
# Velocidad y direcion en X y Y
# random.choice para que tome direciones aleatoria con esa velocidad
enemyX_change = []
enemyY_change = []
numero_de_enemigos = 6

# Game over Texto
over_font = pygame.font.Font('freesansbold.ttf', 32)

# Add-multiples enemigos
for i in range(numero_de_enemigos):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(50, 150))
    # Velocidad y direcion en X y Y
    # random.choice para que tome direciones aleatoria con esa velocidad
    enemyX_change.append(random.choice([3, -3, 3, -3]))
    enemyY_change.append(20)

######Balas#########
# Ready= No puedes ver la bala en la pantalla
# Fire=la bala esta actualmente moviendoce
balaImg = pygame.image.load('bala.png')
balaX = 0
balaY = 490
balaX_change = 0
# Velocidad de disparo
balaY_change = 12
bala_stado = 'ready'

# SCORE
score = 0
tema = pygame.font.Font('freesansbold.ttf', 64)

textoX = 10
textoY = 10


def mostrar_score(x, y):
    ascore = tema.render('score: ' + str(score), True, (255, 255, 255,))
    screen.blit(ascore, (x, y))


def game_over_texto():
    over_texto = tema.render('GAME OVER..', True, (255, 255, 255,))
    screen.blit(over_texto, (200, 250))


# esta funcion plasma el player en las coordenadas x,y
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Esta funcion nos permite cambiar de estado de ready a fire
def dispara_bala(x, y):
    global bala_stado
    bala_stado = 'fire'
    # posicion donde queremos que aparesca la bala
    screen.blit(balaImg, (x + 16, y))
    # print(y)


def colicion(enemyX, enemyY, balaX, balaY):
    # Para hallar la distancia entre el enemigo y la bala usamos la formula
    # de distancia entre dos puntos en este caso la bala y el enemigo
    distancia = math.sqrt((math.pow(enemyX - balaX, 2)) + (math.pow(enemyY - balaY, 2)))
    if distancia < 27:
        return True
    else:
        return False


runing = True

while runing:

    # RGB - RED -GREEN, -BLUE
    screen.fill((0, 0, 0))
    # Fondo
    screen.blit(fondo, (0, 0))
    # playerX += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

        # Pulsacion de teclas left - right
        # KeyDOwn cuando presiono
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bala_stado == 'ready':
                    sonido_bala = mixer.Sound('laser.wav')
                    sonido_bala.play()
                    balaX = playerX
                    dispara_bala(balaX, balaY)

        # KeyDown cuando libero la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 --> 5 = 5 - 0.1
    # 5 = 5 + -0.1
    playerX += playerX_change
    # print(playerX)
    # Para que no se salga de los limites de la pantalla
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(numero_de_enemigos):
        if enemyY[i] > 440:
            for j in range(numero_de_enemigos):
                enemyY[j] = 2000
            game_over_texto()
            break
        enemyX[i] += enemyX_change[i]
        # Para que no se salga de los limites de la pantalla
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Colicion
        Colicion = colicion(enemyX[i], enemyY[i], balaX, balaY)
        if Colicion:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            balaY = 480
            bala_stado = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Movimiento de bala
    # para volverla a la posicion 480 cuando este en la posicion 0
    if balaY <= 0:
        # posicion de disparo
        balaY = 480
        bala_stado = 'ready'

    # Cuando presionamos la barra espaciadora el estado cambia a fire
    # pero por defecto el estado permanece ready
    if bala_stado is 'fire':
        # PERSINTENCIA
        dispara_bala(balaX, balaY)
        balaY -= balaY_change
        # print(balaY)

    player(playerX, playerY)
    mostrar_score(textoX, textoY)
    # lineas que siempre van a estar
    pygame.display.update()
