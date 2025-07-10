import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('images/Fighter Shooter')
icon = pygame.image.load("images/fight.png")
pygame.display.set_icon(icon)

bg_img = pygame.image.load('images/background.png')

font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

ftimage = pygame.image.load('images/arcade-game.png')
enemy_img = pygame.image.load('images/art.png')
bullet_img = pygame.image.load('images/bullet.png')

ftx = 370
fty = 480
ftx_change = 0

enemy_x = []
enemy_y = []
enemy_speed = []
num_enemies = 2

for _ in range(num_enemies):
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 100))
    enemy_speed.append(1)

bullets = []
score = 0
lives = 3
high_score = 0

game_over = False

def show_score():
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

def show_lives():
    screen.blit(font.render(f"Lives: {lives}", True, (255, 0, 0)), (10, 50))

def show_high_score():
    screen.blit(font.render(f"High Score: {high_score}", True, (255, 255, 0)), (550, 10))

def show_game_over():
    screen.blit(over_font.render("GAME OVER", True, (255, 255, 255)), (250, 250))
    screen.blit(font.render("Press R to Restart", True, (200, 200, 200)), (260, 320))

def fire_bullet(x, y):
    bullets.append([x + ftimage.get_width() // 2 - bullet_img.get_width() // 2, y])

def is_collision(ex, ey, bx, by):
    enemy_rect = pygame.Rect(ex, ey, enemy_img.get_width(), enemy_img.get_height())
    bullet_rect = pygame.Rect(bx, by, bullet_img.get_width(), bullet_img.get_height())
    return enemy_rect.colliderect(bullet_rect)

def reset_game():
    global ftx, ftx_change, bullets, enemy_x, enemy_y, score, lives, game_over
    ftx = 370
    ftx_change = 0
    bullets = []
    enemy_x = [random.randint(0, 736) for _ in range(num_enemies)]
    enemy_y = [random.randint(0, 100) for _ in range(num_enemies)]
    score = 0
    lives = 3
    game_over = False

run = True
while run:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ftx_change = -3
                elif event.key == pygame.K_RIGHT:
                    ftx_change = 3
                elif event.key == pygame.K_SPACE:
                    fire_bullet(ftx, fty)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    ftx_change = 0
        elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    if not game_over:
        ftx += ftx_change
        ftx = max(0, min(736, ftx))
        screen.blit(ftimage, (ftx, fty))

        for i in range(num_enemies):
            enemy_y[i] += enemy_speed[i]

            if enemy_y[i] > 440:
                lives -= 1
                enemy_y[i] = 0
                enemy_x[i] = random.randint(0, 736)
                if lives == 0:
                    game_over = True

            for bullet in bullets:
                if is_collision(enemy_x[i], enemy_y[i], bullet[0], bullet[1]):
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        pass
                    score += 1
                    if score > high_score:
                        high_score = score
                    enemy_x[i] = random.randint(0, 736)
                    enemy_y[i] = 0

            screen.blit(enemy_img, (enemy_x[i], enemy_y[i]))

        new_bullets = []
        for bullet in bullets:
            bullet[1] -= 4
            if bullet[1] > 0:
                screen.blit(bullet_img, (bullet[0], bullet[1]))
                new_bullets.append(bullet)
        bullets = new_bullets

        show_score()
        show_lives()
        show_high_score()
    else:
        show_game_over()
        show_high_score()

    pygame.display.update()
