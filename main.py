from aliado import Aliado
from shoot import Shoot
from meteoro import Meteoro, Alien
from jogador import Jogador
import random
import pygame
import os
import sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
###


def main_game():
    pygame.init()
    display = pygame.display.set_mode([840, 480])
    pygame.display.set_caption("Madness in Space")

    objectGroup = pygame.sprite.Group()
    meteorGroup = pygame.sprite.Group()
    alienGroup = pygame.sprite.Group()
    aliadoGroup = pygame.sprite.Group()
    shootGroup = pygame.sprite.Group()

    imagem = pygame.sprite.Sprite(objectGroup)
    imagem.image = pygame.image.load("data/espaco.gif")
    imagem.image = pygame.transform.scale(imagem.image, [840, 480])
    imagem.rect = imagem.image.get_rect()

    jogador = Jogador(objectGroup)

    shoot_sound = pygame.mixer.Sound("data/shoot.wav")

    clock = pygame.time.Clock()
    gameover = False
    timer = 20

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.USEREVENT and "gameover" in event.dict:
                return "gameover"  # Quando um meteoro ou alien ultrapassar a tela, o jogo acaba
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gameover:
                    shoot_sound.play()
                    newshoot = Shoot(objectGroup, shootGroup)
                    newshoot.rect.center = jogador.rect.center

        if not gameover:
            objectGroup.update()

            timer += 1
            if timer > 30:
                timer = 0
                if random.random() < 0.15:  # 15% de chance de spawn de meteoro
                    newMeteor = Meteoro(objectGroup, meteorGroup)
                elif random.random() < 0.15:  # 15% de chance de spawn de alien
                    newAlien = Alien(objectGroup, alienGroup)
                elif random.random() < 0.05:  # 5% de chance de spawn da nave aliada
                    newAliado = Aliado(objectGroup, aliadoGroup)

            collisions = pygame.sprite.spritecollide(jogador, meteorGroup, False, pygame.sprite.collide_mask) or \
                pygame.sprite.spritecollide(
                    jogador, alienGroup, False, pygame.sprite.collide_mask)
            if collisions:
                return "gameover"

            pygame.sprite.groupcollide(
                shootGroup, meteorGroup, True, True, pygame.sprite.collide_mask)
            pygame.sprite.groupcollide(
                shootGroup, alienGroup, True, True, pygame.sprite.collide_mask)

            if pygame.sprite.groupcollide(shootGroup, aliadoGroup, True, True, pygame.sprite.collide_mask):
                return "gameover"  # Se um tiro atingir a nave aliada, o jogo acaba

        display.fill([4, 107, 95])
        objectGroup.draw(display)
        pygame.display.update()


def menu():
    pygame.init()

    pygame.mixer.music.load("data/snes.wav")
    pygame.mixer.music.play(-1)

    display = pygame.display.set_mode([840, 480])
    pygame.display.set_caption("Madness in Space")

    background = pygame.image.load("data/espaco.gif")
    background = pygame.transform.scale(background, [840, 480])

    font = pygame.font.Font(None, 50)
    title_text = font.render("Madness in Space", True, (255, 255, 255))
    start_text = font.render("Start", True, (0, 0, 0))
    start_button = pygame.Rect(340, 250, 160, 50)

    clock = pygame.time.Clock()

    while True:
        display.blit(background, (0, 0))
        display.blit(title_text, (250, 100))
        pygame.draw.rect(display, (255, 255, 255), start_button)
        display.blit(start_text, (380, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"

        pygame.display.update()
        clock.tick(60)


def game_over_screen():
    pygame.init()
    display = pygame.display.set_mode([840, 480])
    pygame.display.set_caption("Game Over")

    background = pygame.image.load("data/espaco.gif")
    background = pygame.transform.scale(background, [840, 480])

    font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_button = pygame.Rect(340, 250, 160, 50)

    clock = pygame.time.Clock()

    while True:
        display.blit(background, (0, 0))
        display.blit(game_over_text, (330, 100))
        pygame.draw.rect(display, (255, 255, 255), restart_button)
        display.blit(restart_text, (360, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart"

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    while True:
        action = menu()
        if action == "quit":
            break
        elif action == "start":
            result = main_game()
            if result == "gameover":
                action = game_over_screen()
                if action == "quit":
                    break
