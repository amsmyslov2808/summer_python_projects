import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (0, 0, 0)
FOREGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Ping pong")

clock = pygame.time.Clock()


BALL_SIZE = 20

ball_dx = 5
ball_dy = 5

ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2

ball = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

is_run = True

while is_run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False

    ball.x += ball_dx
    ball.y += ball_dy

    if ball.y + BALL_SIZE >= SCREEN_HEIGHT or ball.y <= 0:
        ball_dy = -ball_dy

    if ball.x + BALL_SIZE >= SCREEN_WIDTH or ball.x <= 0:
        ball_dx = -ball_dx

    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, FOREGROUND_COLOR, ball)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
