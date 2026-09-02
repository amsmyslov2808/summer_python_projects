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

BALL_DX = 5
BALL_DY = 5

ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2

ball_dx_direction = 1
ball_dy_direction = 1

ball = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_DY = 5

paddle_left_x = 0
paddle_left_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

paddle_right_x = SCREEN_WIDTH - PADDLE_WIDTH
paddle_right_y = paddle_left_y

paddle_left = pygame.Rect(paddle_left_x, paddle_left_y, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(paddle_right_x, paddle_right_y, PADDLE_WIDTH, PADDLE_HEIGHT)

player_left_score = 0
player_right_score = 0

font = pygame.font.Font(None, 60)

is_run = True

while is_run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] == True:
        paddle_left.y -= PADDLE_DY

    if keys[pygame.K_s] == True:
        paddle_left.y += PADDLE_DY

    if paddle_left.y < 0:
        paddle_left.y = 0

    if paddle_left.y + PADDLE_HEIGHT > SCREEN_HEIGHT:
        paddle_left.y = SCREEN_HEIGHT - PADDLE_HEIGHT

    if keys[pygame.K_UP] == True:
        paddle_right.y -= PADDLE_DY

    if keys[pygame.K_DOWN] == True:
        paddle_right.y += PADDLE_DY

    if paddle_right.y < 0:
        paddle_right.y = 0

    if paddle_right.y + PADDLE_HEIGHT > SCREEN_HEIGHT:
        paddle_right.y = SCREEN_HEIGHT - PADDLE_HEIGHT

    ball.x += BALL_DX * ball_dx_direction
    ball.y += BALL_DY * ball_dy_direction

    if ball.y + BALL_SIZE >= SCREEN_HEIGHT or ball.y <= 0:
        ball_dy_direction = -ball_dy_direction

    # if ball.x + BALL_SIZE >= SCREEN_WIDTH or ball.x <= 0:
    #     ball_dx_direction = -ball_dx_direction

    if ball.colliderect(paddle_left):
        ball.x = paddle_left.x + PADDLE_WIDTH + 1
        ball_dx_direction = -ball_dx_direction

    if ball.colliderect(paddle_right):
        ball_x = paddle_right.x - BALL_SIZE - 1
        ball_dx_direction = -ball_dx_direction

    if ball.x < 0:
        player_right_score += 1
        ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2

    if ball.x + BALL_SIZE > SCREEN_WIDTH:
        player_left_score += 1
        ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2

    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, FOREGROUND_COLOR, ball)

    pygame.draw.rect(screen, FOREGROUND_COLOR, paddle_left)
    pygame.draw.rect(screen, FOREGROUND_COLOR, paddle_right)

    pygame.draw.line(
        screen,
        FOREGROUND_COLOR,
        (SCREEN_WIDTH // 2, 0),
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT),
        2,
    )

    score_text = font.render(
        f"{player_left_score}     {player_right_score}",
        True,
        FOREGROUND_COLOR,
    )

    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 40))

    screen.blit(score_text, score_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
