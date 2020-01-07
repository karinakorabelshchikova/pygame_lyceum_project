import pygame
import os
import sys
import tkinter as tk
from tkinter import filedialog
import csv


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


class GameCondition:
    def __init__(self):
        self.music_volume = 1
        self.sound_volume = 1

    def new_game(self, reader):
        pass

    def load_game(self, reader):
        self.music_volume, self.sound_volume = next(reader)
        self.music_volume, self.sound_volume = float(self.music_volume[1:]), float(self.sound_volume)

    def save_game(self, path):
        pass


MUSIC_MENU_FILE_NAME = 'ChadCrouch_TheChorusCeases.mp3'
MUSIC_MAIN_FILE_NAME = 'ChadCrouch_TheLight-filteringCanopy.mp3'

FPS = 30
pygame.init()
pygame.mixer.init()
this_game = GameCondition()
size = width, height = 900, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


class menu_buttons:
    def __init__(self, is_start_menu=True):
        self.menu_sprites = pygame.sprite.Group()

        self.new_game_button = pygame.sprite.Sprite(self.menu_sprites)
        self.new_game_button.image = load_image('новаяигракнопка.png')
        self.new_game_button.rect = self.new_game_button.image.get_rect()
        self.new_game_button.rect.x = 200
        self.new_game_button.rect.y = 190

        self.load_game_button = pygame.sprite.Sprite(self.menu_sprites)
        self.load_game_button.image = load_image('загрузитьигрукнопка.png')
        self.load_game_button.rect = self.load_game_button.image.get_rect()
        self.load_game_button.rect.x = 200
        self.load_game_button.rect.y = 260

        self.music_icon = pygame.sprite.Sprite(self.menu_sprites)
        self.music_icon.image = load_image('музыкаиконка.png', -1)
        self.music_icon.rect = self.load_game_button.image.get_rect()
        self.music_icon.rect.x = 260
        self.music_icon.rect.y = 330

        self.music_plus_button = pygame.sprite.Sprite(self.menu_sprites)
        self.music_plus_button.image = load_image('плюскнопка.png', -1)
        self.music_plus_button.rect = pygame.Rect(230, 355, 40, 40)

        self.music_minus_button = pygame.sprite.Sprite(self.menu_sprites)
        self.music_minus_button.image = load_image('минускнопка.png', -1)
        self.music_minus_button.rect = pygame.Rect(345, 355, 40, 40)

        self.sound_icon = pygame.sprite.Sprite(self.menu_sprites)
        self.sound_icon.image = load_image('звукиконка.png', -1)
        self.sound_icon.rect = self.load_game_button.image.get_rect()
        self.sound_icon.rect.x = 520
        self.sound_icon.rect.y = 330

        self.sound_plus_button = pygame.sprite.Sprite(self.menu_sprites)
        self.sound_plus_button.image = load_image('плюскнопка.png', -1)
        self.sound_plus_button.rect = pygame.Rect(485, 355, 40, 40)

        self.sound_minus_button = pygame.sprite.Sprite(self.menu_sprites)
        self.sound_minus_button.image = load_image('минускнопка.png')
        self.sound_minus_button.rect = pygame.Rect(610, 355, 40, 40)

        if not is_start_menu:
            pass

        self.menu_sprites.draw(screen)


def start_menu():
    pygame.display.set_caption('Мистер герой')
    pygame.mixer.music.load('data/' + MUSIC_MENU_FILE_NAME)
    pygame.mixer.music.play(loops=-1)
    sound = pygame.mixer.Sound('data/buttonclicked.wav')
    screen.blit(load_image('менюзаставка.png'), (0, 0))
    screen.blit(load_image('менюфон.png', -1), (0, 0))
    buttons = menu_buttons()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.new_game_button.rect.collidepoint(event.pos):
                    sound.play()
                    with open('data/newgame.txt', encoding='utf8') as file:
                        reader = csv.reader(file, delimiter=';')
                        this_game.load_game(reader)
                        pygame.mixer.music.fadeout(700)
                        return  # начинаем игру
                elif buttons.load_game_button.rect.collidepoint(event.pos):
                    sound.play()
                    root = tk.Tk()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(title="Выберите слот", filetypes=(("txt files", "*.txt"),))
                    try:
                        with open(file_path, encoding='utf8') as file:
                            reader = csv.reader(file, delimiter=';')
                            this_game.load_game(reader)
                            pygame.mixer.music.fadeout(700)
                            return  # начинаем игру
                    except Exception:
                        pass
                elif buttons.music_plus_button.rect.collidepoint(event.pos):
                    sound.play()
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                elif buttons.music_minus_button.rect.collidepoint(event.pos):
                    sound.play()
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
                    if pygame.mixer.music.get_volume() < 0.1:
                        pygame.mixer.music.set_volume(0)
                elif buttons.sound_plus_button.rect.collidepoint(event.pos):
                    sound.play()
                    sound.set_volume(sound.get_volume() + 0.1)
                elif buttons.sound_minus_button.rect.collidepoint(event.pos):
                    sound.play()
                    sound.set_volume(sound.get_volume() - 0.1)
                    if sound.get_volume() < 0.1:
                        sound.set_volume(0)
                this_game.music_volume = pygame.mixer.music.get_volume()
                this_game.sound_volume = sound.get_volume()


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
