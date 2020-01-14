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
            self.music_icon.image = load_image('музыкаиконка.png')
            self.music_icon.rect = self.music_icon.image.get_rect()
            self.music_icon.rect.x = 260
            self.music_icon.rect.y = 330

            self.music_plus_button = pygame.sprite.Sprite(self.menu_sprites)
            self.music_plus_button.image = load_image('плюскнопка.png')
            self.music_plus_button.rect = pygame.Rect(230, 355, 40, 40)

            self.music_minus_button = pygame.sprite.Sprite(self.menu_sprites)
            self.music_minus_button.image = load_image('минускнопка.png')
            self.music_minus_button.rect = pygame.Rect(345, 355, 40, 40)

            self.sound_icon = pygame.sprite.Sprite(self.menu_sprites)
            self.sound_icon.image = load_image('звукиконка.png')
            self.sound_icon.rect = self.sound_icon.image.get_rect()
            self.sound_icon.rect.x = 520
            self.sound_icon.rect.y = 330

            self.sound_plus_button = pygame.sprite.Sprite(self.menu_sprites)
            self.sound_plus_button.image = load_image('плюскнопка.png')
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
        self.level = self.Level(self, int(next(reader)[0]), reader)

    def load_game(self, reader):
        self.music_volume, self.sound_volume = next(reader)
        self.music_volume, self.sound_volume = float(self.music_volume[1:]), float(self.sound_volume)
        self.level = self.Level(self, int(next(reader)[0]), reader)

    def save_game(self, path):
        pass

    class Level:
        def __init__(self, parent, level_number, reader):
            self.game = parent
            self.all_sprites = pygame.sprite.Group()
            self.camera = parent.Camera(self)
            self.level_number = level_number
            if self.level_number == 1:
                self.hero = eval(next(reader)[0])
                self.all_sprites.add(self.hero)

    class Hero(pygame.sprite.Sprite):
        def __init__(self, level, position, health, special_groups=(), *groups):
            super().__init__(*special_groups, *groups)
            self.level = level  # уровень, к которому привязан герой
            self.health = health  # оставшееся здоровье в процентах
            self.health_sprite = self.Health(health, *groups)  # соответствующий спрайт
            self.Vmax = 20  # оставшееся здоровье в процентах
            self.rect = pygame.Rect(position[0], position[1], 18, 110)
            self.clock = pygame.time.Clock()
            self.waiting = 0  # суммирует время от clock.tick
            self.standing_frame = load_image('геройстоитфрейм.png', -1)
            self.walk_frames = [load_image('геройходьбафрейм1.png', -1),
                                load_image('геройходьбафрейм2.png', -1),
                                load_image('геройходьбафрейм1.png', -1)]
            self.image = self.standing_frame
            self.walk_frames_left = 0
            self.direction = None  # Отвечает за направление падения и ходьбы
            self.Vy = None  # Вертикальная роекция скорости, нужна для падений и прыжков

        class Health(pygame.sprite.Sprite):
            def __init__(self, percent, *groups):
                super().__init__(*groups)

        def move_command(self, doing):
            if self.Vy is None:
                if doing == 'right' or doing == 'left':
                    self.walk_frames_left = 3
                    self.direction = doing
                elif doing == 'up':
                    self.Vy = 40

        def update(self):
            self.clock.tick(self.Vmax)
            if self.Vy is not None:
                if self.Vy <= -50:  # заменить на is_touching_platform()
                    self.direction = None
                    self.Vy = None
                    self.walk_frames_left = 0
                else:
                    if self.direction == 'right':
                        self.rect.x += 10
                    elif self.direction == 'left':
                        self.rect.x -= 10
                    self.rect.y -= self.Vy
                    self.Vy -= 10
            elif False:  # Тут будет проверка, не пора ли падать
                pass  #  И соответствующие действия
            elif self.walk_frames_left:
                self.image = self.walk_frames[-self.walk_frames_left]
                self.walk_frames_left -= 1
                self.rect.x += 10 if self.direction == 'right' else -10
            else:
                self.image = self.standing_frame
                self.direction = None

    class background(pygame.sprite.Sprite):
        def __init__(self, layers):
            super().__init__()

    class Camera(pygame.sprite.Sprite):
        def __init__(self, parent):
            super().__init__()
            self.level = parent

        def update(self):
            pass

    def main_cycle(self):
        pygame.mixer.music.load('data/' + self.MUSIC_MAIN_FILE_NAME)
        pygame.mixer.music.play(loops=-1)

        self.pause_button_group = pygame.sprite.GroupSingle()
        self.pause_button = pygame.sprite.Sprite(self.level.all_sprites, self.pause_button_group)
        self.pause_button.image = load_image('паузакнопка.png', -1)
        self.pause_button.rect = pygame.Rect(830, 10, 60, 60)
        self.pause_button_group.draw(self.screen)

        self.paused = False
        self.time_passed = 0

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
                    elif event.type == pygame.KEYDOWN:
                        if event.scancode == 16:
                            self.level.hero.move_command('action')
                        elif event.scancode == 17:
                            self.level.hero.move_command('up')
                        elif event.scancode == 30:
                            self.level.hero.move_command('left')
                        elif event.scancode == 31:
                            self.level.hero.move_command('down')
                        elif event.scancode == 32:
                            self.level.hero.move_command('right')
            if not self.paused:
                self.screen.blit(load_image('уровень1фон(арки интерьерверх).png'), (0, 0))
                self.level.all_sprites.update()
                self.level.camera.update()
                self.level.all_sprites.draw(self.screen)
            pygame.display.flip()


Game()
