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

    menu_sprites = pygame.sprite.Group()

    new_game_button = pygame.sprite.Sprite(menu_sprites)
    new_game_button.image = load_image('новаяигракнопка.png', -1)
    new_game_button.rect = new_game_button.image.get_rect()
    new_game_button.rect.x = 200
    new_game_button.rect.y = 190

    load_game_button = pygame.sprite.Sprite(menu_sprites)
    load_game_button.image = load_image('загрузитьигрукнопка.png', -1)
    load_game_button.rect = load_game_button.image.get_rect()
    load_game_button.rect.x = 200
    load_game_button.rect.y = 260

    music_icon = pygame.sprite.Sprite(menu_sprites)
    music_icon.image = load_image('музыкаиконка.png', -1)
    music_icon.rect = load_game_button.image.get_rect()
    music_icon.rect.x = 260
    music_icon.rect.y = 330

    music_plus_button = pygame.sprite.Sprite(menu_sprites)
    music_plus_button.image = load_image('плюскнопка.png', -1)
    music_plus_button.rect = pygame.Rect(230, 355, 40, 40)


    music_minus_button = pygame.sprite.Sprite(menu_sprites)
    music_minus_button.image = load_image('минускнопка.png', -1)
    music_minus_button.rect = pygame.Rect(345, 355, 40, 40)

    sound_icon = pygame.sprite.Sprite(menu_sprites)
    sound_icon.image = load_image('звукиконка.png', -1)
    sound_icon.rect = load_game_button.image.get_rect()
    sound_icon.rect.x = 520
    sound_icon.rect.y = 330

    sound_plus_button = pygame.sprite.Sprite(menu_sprites)
    sound_plus_button.image = load_image('плюскнопка.png', -1)
    sound_plus_button.rect = pygame.Rect(485, 355, 40, 40)

    sound_minus_button = pygame.sprite.Sprite(menu_sprites)
    sound_minus_button.image = load_image('минускнопка.png')
    sound_minus_button.rect = pygame.Rect(610, 355, 40, 40)

    menu_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(700)
                    return  # начинаем игру
                elif load_game_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(700)
                    return  # начинаем игру
                elif music_plus_button.rect.collidepoint(event.pos):
                    print('m+')
                elif music_minus_button.rect.collidepoint(event.pos):
                    print('m-')
                elif sound_plus_button.rect.collidepoint(event.pos):
                    print('s+')
                elif sound_minus_button.rect.collidepoint(event.pos):
                    print('s-')
        pygame.display.flip()
        menu_sprites.draw(screen)
        clock.tick(FPS)


start_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    clock.tick()
    pygame.display.flip()
