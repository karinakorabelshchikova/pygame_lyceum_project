import pygame
import os
import sys
import tkinter as tk
from tkinter import filedialog
import csv


def load_image(name, colorkey=None):
    """Функция для загрузки изображений из папки data,
    colorkey=-1 делает места цвета как в позиции (0, 0) прозрачными"""
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
    """Функция отвечает за закрытие программы"""
    pygame.quit()
    sys.exit()


def kill_sprite_group(group):
    """Удаляет все спрайты, находящиеся в данной группе"""
    for sprite in group:
        sprite.kill()


class Game:
    """Главный класс игры"""
    def __init__(self):
        self.MUSIC_MENU_FILE_NAME = 'ChadCrouch_TheChorusCeases.mp3'
        self.MUSIC_MAIN_FILE_NAME = 'ChadCrouch_TheLight-filteringCanopy.mp3'

        self.FPS = 30
        pygame.init()
        pygame.mixer.init()
        self.size = self.width, self.height = 900, 500
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.music_volume = 1
        self.sound_volume = 1

        # sound - звук нажатой кнопки
        self.sound = pygame.mixer.Sound('data/buttonclicked.wav')

        self.start_menu()
        self.main_cycle()

    class menu_buttons:
        """Класс, отвечающий за спрайты-кнопки в стартовом и внутриигровом меню"""
        def __init__(self, screen, is_start_menu=True):
            self.menu_sprites = pygame.sprite.Group()

            if is_start_menu:
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

            else:
                self.save_game_button = pygame.sprite.Sprite(self.menu_sprites)
                self.save_game_button.image = load_image('сохранитьигрукнопка.png')
                self.save_game_button.rect = self.save_game_button.image.get_rect()
                self.save_game_button.rect.x = 200
                self.save_game_button.rect.y = 190

            self.music_icon = pygame.sprite.Sprite(self.menu_sprites)
            self.music_icon.image = load_image('музыкаиконка.png', -1)
            self.music_icon.rect = self.music_icon.image.get_rect()
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
            self.sound_icon.rect = self.sound_icon.image.get_rect()
            self.sound_icon.rect.x = 520
            self.sound_icon.rect.y = 330

            self.sound_plus_button = pygame.sprite.Sprite(self.menu_sprites)
            self.sound_plus_button.image = load_image('плюскнопка.png', -1)
            self.sound_plus_button.rect = pygame.Rect(485, 355, 40, 40)

            self.sound_minus_button = pygame.sprite.Sprite(self.menu_sprites)
            self.sound_minus_button.image = load_image('минускнопка.png')
            self.sound_minus_button.rect = pygame.Rect(610, 355, 40, 40)

            self.menu_sprites.draw(screen)

        def change_volume_probably_pressed(self, game_object, pos):
            """Функция принимает на вход game_object - объект своего родительского класса и координаты нажатия.
            В случае нажатия на одну из кнопок регулирует громкость"""
            if self.music_plus_button.rect.collidepoint(pos):
                game_object.sound.play()
                game_object.music_volume += 0.1
                pygame.mixer.music.set_volume(game_object.music_volume)

            elif self.music_minus_button.rect.collidepoint(pos):
                game_object.sound.play()
                game_object.music_volume -= 0.1
                pygame.mixer.music.set_volume(game_object.music_volume)
                if game_object.music_volume < 0.1:
                    game_object.music_volume = 0
                    pygame.mixer.music.set_volume(0)

            elif self.sound_plus_button.rect.collidepoint(pos):
                game_object.sound.play()
                game_object.sound_volume += 0.1
                game_object.sound.set_volume(game_object.sound_volume)

            elif self.sound_minus_button.rect.collidepoint(pos):
                game_object.sound.play()
                game_object.sound_volume -= 0.1
                game_object.sound.set_volume(game_object.sound_volume)
                if game_object.sound_volume < 0.1:
                    game_object.sound_volume = 0
                    game_object.sound.set_volume(0)

    def start_menu(self):
        pygame.display.set_caption('Мистер герой')
        pygame.display.set_icon(load_image('иконкаокна.png', -1))
        pygame.mixer.music.load('data/' + self.MUSIC_MENU_FILE_NAME)
        pygame.mixer.music.play(loops=-1)
        self.screen.blit(load_image('менюзаставка.png'), (0, 0))
        self.screen.blit(load_image('менюфон.png', -1), (0, 0))
        buttons = self.menu_buttons(self.screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons.new_game_button.rect.collidepoint(event.pos):
                        self.sound.play()
                        with open('data/newgame.txt', encoding='utf8') as file:
                            reader = csv.reader(file, delimiter=';')
                            self.load_game(reader)
                            pygame.mixer.music.fadeout(700)
                            kill_sprite_group(buttons.menu_sprites)
                            return  # начинаем игру
                    elif buttons.load_game_button.rect.collidepoint(event.pos):
                        self.sound.play()
                        root = tk.Tk()
                        root.withdraw()
                        file_path = filedialog.askopenfilename(title="Выберите слот",
                                                               filetypes=(("txt files", "*.txt"),))
                        try:
                            with open(file_path, encoding='utf8') as file:
                                reader = csv.reader(file, delimiter=';')
                                self.load_game(reader)
                                pygame.mixer.music.fadeout(700)
                                kill_sprite_group(buttons.menu_sprites)
                                return  # начинаем игру
                        except Exception:
                            pass
                    buttons.change_volume_probably_pressed(self, event.pos)

    def new_game(self, reader):
        self.level_number = 1
        self.get_level()
        self.all_sprites = pygame.sprite.Group()
        self.get_changeable(reader)

    def load_game(self, reader):
        self.music_volume, self.sound_volume = next(reader)
        self.music_volume, self.sound_volume = float(self.music_volume[1:]), float(self.sound_volume)
        self.level_number = int(next(reader)[0])
        self.get_level()
        self.all_sprites = pygame.sprite.Group()
        self.get_changeable(reader)

    def save_game(self, path):
        pass

    def get_level(self):
        if self.level_number == 1:
            pass

    class Hero(pygame.sprite.Sprite):
        def __init__(self, position, health, special_groups=(), *groups):
            super().__init__(*special_groups, *groups)
            self.health = health
            self.health_sprite = self.Health(*groups)

        class Health(pygame.sprite.Sprite):
            def __init__(self, percent, *groups):
                super().__init__(*groups)

        def move(self, doing):
            pass

        def update(self):
            pass

    class background(pygame.sprite.Sprite):
        def __init__(self, layers):
            super().__init__()

    class Camera(pygame.sprite.Sprite):
        def __init__(self, parent):
            super().__init__()
            self.game = parent

        def update(self):
            pass

    def get_changeable(self, reader):
        if self.level_number == 1:
            self.hero = eval(next(reader)[0])
            self.all_sprites.add(self.hero)
        print(self.all_sprites)
        print(self.hero.health)

    def main_cycle(self):
        pygame.mixer.music.load('data/' + self.MUSIC_MAIN_FILE_NAME)
        pygame.mixer.music.play(loops=-1)

        # delete later
        self.screen.fill(pygame.color.Color('black'))

        self.pause_button_group = pygame.sprite.GroupSingle()
        self.pause_button = pygame.sprite.Sprite(self.pause_button_group)
        self.pause_button.image = load_image('паузакнопка.png', -1)
        self.pause_button.rect = pygame.Rect(830, 10, 60, 60)
        self.pause_button_group.draw(self.screen)

        self.paused = False
        self.camera = self.Camera(self)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_button.rect.collidepoint(event.pos):
                            self.sound.play()
                            self.paused = False
                            kill_sprite_group(self.buttons.menu_sprites)
                        else:
                            self.buttons.change_volume_probably_pressed(self, event.pos)
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_button.rect.collidepoint(event.pos):
                            self.sound.play()
                            self.paused = True
                            self.buttons = self.menu_buttons(self.screen, is_start_menu=False)
                        else:
                            # attack
                            pass
                    elif event.type == pygame.K_a:
                        self.hero.move('left')
                    elif event.type == pygame.K_w:
                        self.hero.move('up')
                    elif event.type == pygame.K_d:
                        self.hero.move('right')
                    elif event.type == pygame.K_w:
                        self.hero.move('down')
                    elif event.type == pygame.K_q:
                        self.hero.move('action')
                    self.all_sprites.update()
                    self.camera.update()
            self.clock.tick(self.FPS)
            pygame.display.flip()


Game()
