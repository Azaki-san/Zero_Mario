import pygame
import pygame_gui
import os
import sys
import time
from random import randrange, choice


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(0, 0)

    def update_pos(self, x, y):
        if 0 <= x <= 940 and 0 <= y <= 524:
            self.rect.x = x
            self.rect.y = y


class Bowser(pygame.sprite.Sprite):  # класс злодея
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = bowser_image
        self.rect = self.image.get_rect().move(914, 0)
        self.down = True
        self.speed = 1.75
        self.is_paused = False
        self.is_touched = False

    def switch_pause(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def update(self, *args):
        if not self.is_paused:
            if self.down and self.rect.y + self.speed <= 514:  # вылет за границу
                self.rect.y += self.speed
            else:
                self.down = False
                if self.rect.y - self.speed >= 0:
                    self.rect.y -= self.speed
                else:
                    self.down = True
            if pygame.sprite.collide_mask(self, player):
                self.is_touched = True
                ora()


class Bullet(pygame.sprite.Sprite):  # класс пули
    def __init__(self):
        y1 = bowser.rect.y
        super().__init__(player_group, all_sprites)
        self.image = pulya_image
        self.image = pygame.transform.scale(self.image, (40, 25))
        self.rect = self.image.get_rect().move(914, y1)
        self.mask = pygame.mask.from_surface(self.image)
        self.killed = False
        self.is_paused = False
        self.speed = 4

    def switch_pause(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def update(self, *args):
        if not self.is_paused:
            if not pygame.sprite.collide_mask(self, player):
                self.rect.x -= self.speed
            else:
                self.killed = True


class Box(pygame.sprite.Sprite):
    def __init__(self):
        y1 = bowser.rect.y
        super().__init__(player_group, all_sprites)
        self.image = box_image
        self.rect = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect().move(1000, randrange(80, 535))
        self.mask = pygame.mask.from_surface(self.image)
        self.is_paused = False
        self.speed = 8
        self.touched = False
        self.isActive = True

    def switch_pause(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def update(self, *args):
        if not self.is_paused:
            if not pygame.sprite.collide_mask(self, player):
                self.rect.x -= self.speed
                if self.rect.x < 0:
                    self.isActive = False
            else:
                self.touched = True
                self.isActive = False
                self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        y1 = bowser.rect.y
        super().__init__(player_group, all_sprites)
        self.image = monetka_image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect().move(914, y1)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_paused = False
        self.touched = False
        self.speed = 4

    def switch_pause(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def update(self, *args):
        if not self.is_paused:
            if not pygame.sprite.collide_mask(self, player):
                self.rect.x -= self.speed
            else:
                change_score()
                self.touched = True
                self.kill()


def load_image(name):
    fullname = os.path.join('data\images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def confirmation_exit(manager_):  # окошко с подтверждением выхода
    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((375, 200), (300, 200)),
        manager=manager_,
        window_title='Confirmation',
        action_long_desc='Do you want to exit?',
        action_short_name='OK',
        blocking=True
    )


def start_window():  # самая первая функция для главного экрана
    manager = pygame_gui.UIManager(size)
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((750, 300), (200, 60)),
        text='Start',
        manager=manager
    )

    entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((750, 270), (200, 60)),
        manager=manager
    )

    game_mode = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['Mix', 'Catch', 'Avoid'], starting_option='Mix',
        relative_rect=pygame.Rect((750, 230), (200, 40)),
        manager=manager
    )

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((750, 365), (200, 60)),
        text='Exit Game',
        manager=manager
    )

    while True:
        screen.blit(fon, (0, 0))
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_exit(manager)
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    terminate()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        return entry.text, game_mode.selected_option
                    if event.ui_element == exit_button:
                        confirmation_exit(manager)
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


def change_score(plus=1):
    global score, top_score

    '''В этой функции происходит смена очков, требуется проверка на режим игры'''
    score += plus
    if score > top_score:
        top_score = score
        with open('data/top_score.txt', 'rt') as txt:
            b = txt.readlines()
        b_2 = []
        for i in b:
            b_2.append(''.join(i.split('\n')))
        if g_mode == 'Mix':
            b_2[0] = str(top_score)
        elif g_mode == 'Catch':
            b_2[1] = str(top_score)
        else:
            b_2[2] = str(top_score)
        with open('data/top_score.txt', 'wt') as txt:
            print(b_2)
            txt.write('\n'.join(b_2))


def start_music():
    global j, flag_j, bowser_image, j_mode, s

    main_theme.stop()

    j = pygame.mixer.Sound('data/music/secret.ogg')
    j.play()

    bowser_image = load_image('d.png')
    bowser.image = bowser_image
    bowser.rect = bowser.image.get_rect().move(bowser.rect.x, bowser.rect.top)

    player_image = load_image('j.png')
    s = 8
    player.image = player_image
    player.rect = player.image.get_rect().move(player.rect.x, player.rect.top)

    flag_j = True
    j_mode = True


def ora():
    global j, ora_

    if not ora_:
        j.stop()
        haha = pygame.mixer.Sound('data/music/ora.ogg')
        haha.play()
        ora_ = True
        bowser.speed = 0


def game(name, g_mode):  # функция игры!!
    global s, ora_

    ora_ = False

    manager = pygame_gui.UIManager(size)
    level = 1
    flag_here = False
    pause = False
    run = True
    bull_c = 0
    coin_c = 0
    special_coin_c = 0
    box_c = 0
    j_c = 0
    b_box = False
    secret_fon = False
    secret_secret_fon = False
    f_s = load_image('jo_secret.png')

    save_pul = []
    save_mon = []
    ha = False

    last_time_ms = int(round(time.time() * 1000))
    while run:
        if 20 > score >= 10:
            ha = True
            level = 2
        if 30 > score >= 20:
            ha = True
            level = 3
        if score >= 40:
            ha = True
            level = 4

        if ha and not ora_:
            ha = False
            bowser.speed = 1.75 + 2 * (level - 1)
            for i in save_pul:
                i.speed = 4 + (level - 1) * 1
            for i in save_mon:
                i.speed = 4 + (level - 1) * 1
        if not ora_:
            for i in save_pul:
                if i.killed:
                    run = False
        diff_time_ms = int(round(time.time() * 1000)) - last_time_ms
        if ora_:
            change_score(3)
        if diff_time_ms >= 400:
            if ora_:
                j_c += 1
            bull_c += 1
            coin_c += 1
            box_c += 1
            special_coin_c += 1
            last_time_ms = int(round(time.time() * 1000))
        if j_c == 40:
            return

        '''r, f - переменные с какой периодичностью будут появляться объекты'''
        if level == 1:
            r, f = 4, 10
        elif level == 2:
            r, f = 3, 8
        elif level == 3:
            r, f = 2, 6
        elif level == 4:
            r, f = 2, 5

        hmm = randrange(r, f)
        if bull_c == hmm and not pause and (g_mode == 'Mix' or g_mode == 'Avoid'):
            bull_c = 0
            save_pul.append(Bullet())
        if box_c == randrange(20, 40):
            if not ora_:
                s = 4
            box_c = 0
            if not b_box or not b_box.isActive:
                b_box = Box()
        if b_box:  # коробка и её проверка
            if b_box.touched:
                b_box = False
                haha = ['SPEEDUP', '+ 10 SCORE', 'О, повезло повезло', 'JOJO reference']
                cho = choice(haha)
                if cho == haha[0]:
                    s = 8
                if cho == haha[1]:
                    change_score(10)
                if cho == haha[2]:
                    secret_fon = True
                if cho == haha[3]:
                    if not flag_j:
                        start_music()
                        secret_secret_fon = True

        if g_mode == 'Avoid' and not pause:
            save_delete = []
            for i in save_pul:
                if i.rect.x < 0:
                    change_score()
                    save_delete.append(i)
            for i in save_delete:
                save_pul.remove(i)
            if special_coin_c == randrange(10, 25):
                special_coin_c = 0
                save_mon.append(Coin())
            for i in save_mon:
                if i.touched:
                    change_score(10)
                    save_mon.remove(i)

        q = hmm
        if b_box and pause and not b_box.is_paused:
            b_box.switch_pause()

        q = randrange(r, f)

        if coin_c == q and not pause and (g_mode == 'Mix' or g_mode == 'Catch'):
            coin_c = 0
            save_mon.append(Coin())
            if g_mode == 'Catch':
                if len(save_mon) % 5 == 0:
                    save_pul.append(Bullet())

        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bowser.switch_pause()
                    for i in save_pul:
                        i.switch_pause()
                    for j in save_mon:
                        j.switch_pause()
                    if b_box:
                        b_box.switch_pause()
                    pause = not pause

        keys = pygame.key.get_pressed()

        if not pause:
            if bowser.is_paused:
                bowser.switch_pause()
            if keys[pygame.K_UP]:
                player.update_pos(player.rect.x, player.rect.y - s)
            if keys[pygame.K_DOWN]:
                player.update_pos(player.rect.x, player.rect.y + s)
            if j_mode:
                if keys[pygame.K_LEFT]:
                    player.update_pos(player.rect.x - s, player.rect.y)
                if keys[pygame.K_RIGHT]:
                    player.update_pos(player.rect.x + s, player.rect.y)
        else:
            pause_text = font_pause.render('PAUSED', True, pause_color)
            pause_text_rect = pause_text.get_rect()
            pause_text_rect.top = 200
            pause_text_rect.x = 375
            screen.blit(pause_text, pause_text_rect)

            player_text = font.render('PLAYER: ' + str(name), True, pause_color)
            player_text_rect = player_text.get_rect()
            player_text_rect.top = 300
            player_text_rect.x = 300
            screen.blit(player_text, player_text_rect)

        level_text = font.render('Level: ' + str(level), True, level_color)
        level_text_rect = level_text.get_rect()
        level_text_rect.top = -25
        level_text_rect.x = 120
        screen.blit(level_text, level_text_rect)

        score_text = font.render('Score: ' + str(score), True, score_color)
        score_text_rect = score_text.get_rect()
        score_text_rect.top = -25
        score_text_rect.x = 320
        screen.blit(score_text, score_text_rect)

        top_score_text = font.render('Top Score: ' + str(top_score), True, top_score_color)
        top_score_text_rect = top_score_text.get_rect()
        top_score_text_rect.top = -25
        top_score_text_rect.x = 570
        screen.blit(top_score_text, top_score_text_rect)

        pygame.display.update()
        if secret_secret_fon:
            screen.blit(f_s, (0, 0))
        elif not secret_fon:
            if level == 1:
                screen.blit(fon_level1, (0, 0))
            elif level == 2:
                screen.blit(fon_level2, (0, 0))
            elif level == 3:
                screen.blit(fon_level3, (0, 0))
            elif level == 4:
                screen.blit(fon_level4, (0, 0))

        else:
            if not flag_here:
                flag_here = True
                choice_pls = randrange(1, 3)
                if choice_pls == 1:
                    fon_secret = load_image('secret_fon.jpg')
                else:
                    fon_secret = load_image('secret_fon2.jpg')
            screen.blit(fon_secret, (0, 0))

        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(60)
        manager.update(time_delta)
        manager.draw_ui(screen)


def terminate():
    pygame.quit()
    sys.exit()


s = 4

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Zero Mario')
    size = WIDTH, HEIGHT = 1000, 600

    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (WIDTH, HEIGHT))
    fon_level1 = pygame.transform.scale(load_image('level1.jpg'), (WIDTH, HEIGHT))
    fon_level2 = pygame.transform.scale(load_image('level2.jpg'), (WIDTH, HEIGHT))
    fon_level3 = pygame.transform.scale(load_image('level3.jpg'), (WIDTH, HEIGHT))
    fon_level4 = pygame.transform.scale(load_image('level4.jpg'), (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font('data/fonts/font_now.otf', 30)
    font_pause = pygame.font.Font('data/fonts/font_now.otf', 45)
    level_color = pygame.color.Color('green')
    score_color = pygame.color.Color('brown')
    top_score_color = pygame.color.Color('red')
    pause_color = pygame.color.Color('white')
    player = False
    bowser = False

    pulya_image = load_image("1.png")
    monetka_image = load_image('monetka.png')
    box_image = load_image('box.png')
    main_theme = pygame.mixer.Sound('data/music/main_theme.ogg')
    end_theme = pygame.mixer.Sound('data/music/end_theme.ogg')
    flag_j = False
    while True:
        j_mode = False
        player_image = load_image('mar.png')
        bowser_image = load_image('bowser2.png')

        all_sprites = pygame.sprite.Group()
        pulya_group = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        if flag_j:
            j.stop()
        flag_j = False

        end_theme.stop()
        main_theme.play()

        name, g_mode = start_window()

        score = 0
        with open('data/top_score.txt', 'r') as txt:
            if g_mode == 'Mix':
                a = txt.readlines()[0]
            elif g_mode == 'Catch':
                a = txt.readlines()[1]
            else:
                a = txt.readlines()[2]
        top_score = int(a)
        level = 1

        player = Player()
        bowser = Bowser()

        game(name, g_mode)
        main_theme.stop()
        end_theme.play()

        fon2 = pygame.transform.scale(load_image('game_over.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon2, (0, 0))

        flag = False
        while True:
            if flag:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    flag = True
            pygame.display.flip()
