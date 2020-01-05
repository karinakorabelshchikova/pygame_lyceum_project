import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


MUSIC_MENU_FILE_NAME = 'ChadCrouch_TheChorusCeases.mp3'
MUSIC_MAIN_FILE_NAME = 'ChadCrouch_TheLight-filteringCanopy.mp3'

FPS = 30
pygame.init()
pygame.mixer.pre_init(frequency=88000, size=-16, channels=2, buffer=512)
pygame.mixer.init()
size = width, height = 900, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
music = 0
sounds = 0


def start_menu():
    pygame.mixer.music.load('data/' + MUSIC_MENU_FILE_NAME)
    pygame.mixer.music.play(loops=-1)
    screen.blit(load_image('менюзаставка.png'), (0, 0))
    screen.blit(load_image('менюфон.png', -1), (0, 0))

    menu_buttons_sprites = pygame.sprite.Group()
    new_game_button = pygame.sprite.Sprite(menu_buttons_sprites)
    new_game_button.image = load_image('новаяигракнопка.png', -1)
    new_game_button.rect = new_game_button.image.get_rect()
    new_game_button.rect.x = 200
    new_game_button.rect.y = 190
    load_game_button = pygame.sprite.Sprite(menu_buttons_sprites)
    load_game_button.image = load_image('загрузитьигрукнопка.png', -1)
    load_game_button.rect = load_game_button.image.get_rect()
    load_game_button.rect.x = 200
    load_game_button.rect.y = 260
    menu_buttons_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.fadeout(500)
                return  # начинаем игру
        pygame.display.flip()
        menu_buttons_sprites.draw(screen)
        clock.tick(FPS)


start_menu()
print(1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    clock.tick()
    pygame.display.flip()
