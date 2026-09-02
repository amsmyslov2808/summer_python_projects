import pygame  # Подключаем библиотеку Pygame

pygame.init()  # Запускаем и подготавливаем все модули Pygame

WIDTH = 800  # Задаём ширину игрового окна
HEIGHT = 500  # Задаём высоту игрового окна

BLACK = (0, 0, 0)  # Создаём чёрный цвет в формате RGB
WHITE = (255, 255, 255)  # Создаём белый цвет в формате RGB

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаём игровое окно
pygame.display.set_caption("Pong")  # Устанавливаем название окна

clock = pygame.time.Clock()  # Создаём объект для управления скоростью игры

PADDLE_WIDTH = 15  # Задаём ширину ракетки
PADDLE_HEIGHT = 100  # Задаём высоту ракетки
PADDLE_SPEED = 6  # Задаём скорость движения ракеток

BALL_SIZE = 20  # Задаём ширину и высоту мяча
BALL_SPEED_X = 5  # Задаём скорость мяча по горизонтали
BALL_SPEED_Y = 5  # Задаём скорость мяча по вертикали

left_paddle = pygame.Rect(30, 200, PADDLE_WIDTH, PADDLE_HEIGHT)  # Создаём левую ракетку
right_paddle = pygame.Rect(
    755, 200, PADDLE_WIDTH, PADDLE_HEIGHT
)  # Создаём правую ракетку

ball = pygame.Rect(390, 240, BALL_SIZE, BALL_SIZE)  # Создаём мяч в центре экрана

ball_speed_x = BALL_SPEED_X  # Сохраняем текущую скорость мяча по горизонтали
ball_speed_y = BALL_SPEED_Y  # Сохраняем текущую скорость мяча по вертикали

left_score = 0  # Создаём счёт левого игрока
right_score = 0  # Создаём счёт правого игрока

font = pygame.font.Font(None, 60)  # Создаём шрифт для отображения счёта

running = True  # Создаём переменную, которая отвечает за работу игры

while running:  # Запускаем главный игровой цикл
    for event in pygame.event.get():  # Получаем все события пользователя
        if event.type == pygame.QUIT:  # Проверяем, нажал ли пользователь на крестик
            running = False  # Останавливаем главный игровой цикл

    keys = pygame.key.get_pressed()  # Получаем информацию о нажатых клавишах

    if keys[pygame.K_w]:  # Проверяем, нажата ли клавиша W
        left_paddle.y -= PADDLE_SPEED  # Двигаем левую ракетку вверх

    if keys[pygame.K_s]:  # Проверяем, нажата ли клавиша S
        left_paddle.y += PADDLE_SPEED  # Двигаем левую ракетку вниз

    if keys[pygame.K_UP]:  # Проверяем, нажата ли стрелка вверх
        right_paddle.y -= PADDLE_SPEED  # Двигаем правую ракетку вверх

    if keys[pygame.K_DOWN]:  # Проверяем, нажата ли стрелка вниз
        right_paddle.y += PADDLE_SPEED  # Двигаем правую ракетку вниз

    if left_paddle.top < 0:  # Проверяем, вышла ли левая ракетка за верхнюю границу
        left_paddle.top = 0  # Возвращаем ракетку к верхней границе

    if (
        left_paddle.bottom > HEIGHT
    ):  # Проверяем, вышла ли левая ракетка за нижнюю границу
        left_paddle.bottom = HEIGHT  # Возвращаем ракетку к нижней границе

    if right_paddle.top < 0:  # Проверяем, вышла ли правая ракетка за верхнюю границу
        right_paddle.top = 0  # Возвращаем ракетку к верхней границе

    if (
        right_paddle.bottom > HEIGHT
    ):  # Проверяем, вышла ли правая ракетка за нижнюю границу
        right_paddle.bottom = HEIGHT  # Возвращаем ракетку к нижней границе

    ball.x += ball_speed_x  # Передвигаем мяч по горизонтали
    ball.y += ball_speed_y  # Передвигаем мяч по вертикали

    if ball.top <= 0:  # Проверяем столкновение мяча с верхней стеной
        ball.top = 0  # Возвращаем мяч внутрь игрового окна
        ball_speed_y = -ball_speed_y  # Меняем направление движения мяча по вертикали

    if ball.bottom >= HEIGHT:  # Проверяем столкновение мяча с нижней стеной
        ball.bottom = HEIGHT  # Возвращаем мяч внутрь игрового окна
        ball_speed_y = -ball_speed_y  # Меняем направление движения мяча по вертикали

    if ball.colliderect(left_paddle):  # Проверяем столкновение мяча с левой ракеткой
        ball.left = left_paddle.right  # Перемещаем мяч за границу левой ракетки
        ball_speed_x = abs(ball_speed_x)  # Направляем мяч вправо

    if ball.colliderect(right_paddle):  # Проверяем столкновение мяча с правой ракеткой
        ball.right = right_paddle.left  # Перемещаем мяч за границу правой ракетки
        ball_speed_x = -abs(ball_speed_x)  # Направляем мяч влево

    if ball.right < 0:  # Проверяем, улетел ли мяч за левую границу
        right_score += 1  # Добавляем очко правому игроку
        ball.center = (WIDTH // 2, HEIGHT // 2)  # Возвращаем мяч в центр экрана
        ball_speed_x = BALL_SPEED_X  # Направляем мяч вправо
        ball_speed_y = BALL_SPEED_Y  # Устанавливаем начальную вертикальную скорость

    if ball.left > WIDTH:  # Проверяем, улетел ли мяч за правую границу
        left_score += 1  # Добавляем очко левому игроку
        ball.center = (WIDTH // 2, HEIGHT // 2)  # Возвращаем мяч в центр экрана
        ball_speed_x = -BALL_SPEED_X  # Направляем мяч влево
        ball_speed_y = BALL_SPEED_Y  # Устанавливаем начальную вертикальную скорость

    screen.fill(BLACK)  # Закрашиваем весь экран чёрным цветом

    pygame.draw.rect(screen, WHITE, left_paddle)  # Рисуем левую ракетку
    pygame.draw.rect(screen, WHITE, right_paddle)  # Рисуем правую ракетку
    pygame.draw.ellipse(screen, WHITE, ball)  # Рисуем круглый мяч

    pygame.draw.line(  # Начинаем рисовать центральную линию
        screen,  # Указываем окно, в котором рисуем
        WHITE,  # Указываем цвет линии
        (WIDTH // 2, 0),  # Указываем начальную точку линии
        (WIDTH // 2, HEIGHT),  # Указываем конечную точку линии
        2,  # Указываем толщину линии
    )  # Завершаем команду рисования линии

    score_text = font.render(  # Создаём изображение с текстом счёта
        f"{left_score}     {right_score}",  # Формируем строку со счётом игроков
        True,  # Включаем сглаживание текста
        WHITE,  # Указываем белый цвет текста
    )  # Завершаем создание изображения с текстом

    score_rect = score_text.get_rect(  # Получаем прямоугольную область текста
        center=(WIDTH // 2, 40)  # Размещаем центр текста в верхней части экрана
    )  # Завершаем настройку положения текста

    screen.blit(score_text, score_rect)  # Выводим счёт на экран

    pygame.display.flip()  # Показываем на экране нарисованный игровой кадр

    clock.tick(60)  # Ограничиваем игру до 60 кадров в секунду

pygame.quit()  # Завершаем работу Pygame после выхода из цикла
