import pygame
import os
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(0, 0)

    def update_pos(self, x, y):
        if 0 <= x <= 940 and 0 <= y <= 524:
            self.rect.x = x
            self.rect.y = y


class Bowser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = bowser_image
        self.rect = self.image.get_rect().move(914, 0)
        self.down = True
        self.speed = 1.75

    def update(self, *args):
        if self.down and self.rect.y + self.speed <= 514:
            self.rect.y += self.speed
        else:
            self.down = False
            if self.rect.y - self.speed >= 0:
                self.rect.y -= self.speed
            else:
                self.down = True


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_window():  # самая первая функция для главного экрана
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

s = 2

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Mario Game v0.0001')
    size = WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (WIDTH, HEIGHT))
    fon_level1 = pygame.transform.scale(load_image('level1.jpg'), (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font('data/font_now.otf', 30)
    level_color = pygame.color.Color('green')
    score_color = pygame.color.Color('brown')
    top_score_color = pygame.color.Color('red')

    start_window()

    score = 0
    top_score = 0
    level = 1

    player_image = load_image('mar.png')
    bowser_image = load_image('bowser2.png')
    player = Player()
    bowser = Bowser()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player.update_pos(player.rect.x, player.rect.y - s)
        if keys[pygame.K_DOWN]:
            player.update_pos(player.rect.x, player.rect.y + s)
        if keys[pygame.K_LEFT]:
            player.update_pos(player.rect.x - s, player.rect.y)
        if keys[pygame.K_RIGHT]:
            player.update_pos(player.rect.x + s, player.rect.y)



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
        top_score_text_rect.x = 535
        screen.blit(top_score_text, top_score_text_rect)

        pygame.display.update()
        screen.blit(fon_level1, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(60)

