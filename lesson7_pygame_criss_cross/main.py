import pygame

# Инициализируем все подключённые модули pygame.
# Это нужно сделать до создания окна, шрифтов и других объектов pygame.
pygame.init()

# -----------------------------
# РАЗМЕРЫ ОКНА И ИГРОВОГО ПОЛЯ
# -----------------------------

# Ширина и высота всего окна в пикселях.
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

# Игровое поле представляет собой квадрат размером 600 на 600 пикселей.
FIELD_SIZE = 600

# В одной строке и одном столбце находится по три клетки.
# Целочисленное деление // вычисляет размер одной клетки: 600 // 3 = 200.
COUNT_CELLS = 3
CELL_SIZE = FIELD_SIZE // COUNT_CELLS

# Свободное пространство между игровым полем и границами окна.
HORIZONTAL_MARGIN = 50
VERTICAL_MARGIN = 100

# Координаты левого верхнего угла игрового поля.
# В pygame координата X увеличивается вправо, а координата Y — вниз.
FIELD_X = HORIZONTAL_MARGIN
FIELD_Y = VERTICAL_MARGIN

# Отступ крестика от краёв клетки и толщина его линий.
X_MARGIN = 40
X_WIDTH = 12

# Радиус нолика и толщина линии его окружности.
O_RADIUS = 60
O_WIDTH = 12

# -----------------------------
# ЦВЕТА
# -----------------------------

# Каждый цвет задаётся кортежем RGB: (красный, зелёный, синий).
# Значение каждого компонента находится в диапазоне от 0 до 255.
BACKGROUND_COLOR = (30, 35, 50)
FIELD_COLOR = (50, 60, 80)
LINE_COLOR = (100, 120, 150)

X_COLOR = (255, 90, 120)
O_COLOR = (70, 200, 255)

TEXT_REGULAR_COLOR = (255, 255, 255)
TEXT_WIN_COLOR = (80, 220, 140)

# -----------------------------
# СОЗДАНИЕ ОКНА, ЧАСОВ И ШРИФТОВ
# -----------------------------

# Создаём окно pygame и получаем поверхность screen.
# На этой поверхности ниже будут рисоваться все элементы игры.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Устанавливаем текст, который отображается в заголовке окна.
pygame.display.set_caption("Крестики-нолики")

# Объект Clock позволит ограничить скорость главного цикла,
# чтобы игра не использовала процессор без необходимости.
clock = pygame.time.Clock()

# None означает стандартный шрифт pygame, а числа задают его размер.
# Большой шрифт используется сверху, маленький — для подсказки снизу.
top_font = pygame.font.Font(None, 50)
bottom_font = pygame.font.Font(None, 35)

# -----------------------------
# СОСТОЯНИЕ ИГРЫ
# -----------------------------

# Эти константы задают значения, которые могут храниться в клетке.
# Точка означает свободную клетку, X — крестик, O — нолик.
EMPTY_SIGN = "."
X_SIGN = "X"
O_SIGN = "O"

# Двумерный список 3 на 3 хранит состояние игрового поля.
# Первый индекс обозначает строку, второй — столбец:
# field[0][0] — верхняя левая клетка,
# field[2][2] — нижняя правая клетка.
field = [
    [EMPTY_SIGN, EMPTY_SIGN, EMPTY_SIGN],
    [EMPTY_SIGN, EMPTY_SIGN, EMPTY_SIGN],
    [EMPTY_SIGN, EMPTY_SIGN, EMPTY_SIGN],
]

# В начале новой партии первым ходит игрок X.
current_player = X_SIGN

# Эти строки будут показаны над и под игровым полем.
top_text_value = "Ход игрока: X"
bottom_text_value = "R - начать заново"

# Пока партия продолжается, верхняя надпись имеет обычный белый цвет.
# После победы или ничьей цвет будет заменён на TEXT_WIN_COLOR.
top_text_color = TEXT_REGULAR_COLOR

# is_run отвечает за работу всего приложения:
# False означает, что нужно выйти из главного цикла и закрыть окно.
is_run = True

# is_run_current_game отвечает только за текущую партию:
# после победы или ничьей становится False и блокирует новые ходы,
# однако окно остаётся открытым и пользователь может нажать R.
is_run_current_game = True


def check_winner():
    """Проверяет текущее состояние игрового поля.

    Возвращает X_SIGN или O_SIGN, если один из игроков победил.
    Возвращает строку "Ничья", если свободных клеток больше нет.
    Возвращает строку "none", если партию нужно продолжать.
    """

    # У игрока есть восемь возможных выигрышных комбинаций:
    # три горизонтальные строки, три вертикальных столбца
    # и две диагонали. Сначала проверяем все комбинации для X.
    # Оператор and связывает клетки одной комбинации,
    # а оператор or отделяет одну выигрышную комбинацию от другой.
    if (
        field[0][0] == X_SIGN
        and field[0][1] == X_SIGN
        and field[0][2] == X_SIGN
        or field[1][0] == X_SIGN
        and field[1][1] == X_SIGN
        and field[1][2] == X_SIGN
        or field[2][0] == X_SIGN
        and field[2][1] == X_SIGN
        and field[2][2] == X_SIGN
        or field[0][0] == X_SIGN
        and field[1][0] == X_SIGN
        and field[2][0] == X_SIGN
        or field[0][1] == X_SIGN
        and field[1][1] == X_SIGN
        and field[2][1] == X_SIGN
        or field[0][2] == X_SIGN
        and field[1][2] == X_SIGN
        and field[2][2] == X_SIGN
        or field[0][0] == X_SIGN
        and field[1][1] == X_SIGN
        and field[2][2] == X_SIGN
        or field[0][2] == X_SIGN
        and field[1][1] == X_SIGN
        and field[2][0] == X_SIGN
    ):
        return X_SIGN

    # Если X не победил, проверяем те же восемь комбинаций для O.
    elif (
        field[0][0] == O_SIGN
        and field[0][1] == O_SIGN
        and field[0][2] == O_SIGN
        or field[1][0] == O_SIGN
        and field[1][1] == O_SIGN
        and field[1][2] == O_SIGN
        or field[2][0] == O_SIGN
        and field[2][1] == O_SIGN
        and field[2][2] == O_SIGN
        or field[0][0] == O_SIGN
        and field[1][0] == O_SIGN
        and field[2][0] == O_SIGN
        or field[0][1] == O_SIGN
        and field[1][1] == O_SIGN
        and field[2][1] == O_SIGN
        or field[0][2] == O_SIGN
        and field[1][2] == O_SIGN
        and field[2][2] == O_SIGN
        or field[0][0] == O_SIGN
        and field[1][1] == O_SIGN
        and field[2][2] == O_SIGN
        or field[0][2] == O_SIGN
        and field[1][1] == O_SIGN
        and field[2][0] == O_SIGN
    ):
        return O_SIGN
    else:
        # Если ни один игрок не победил, проверяем возможность ничьей.
        # Для этого считаем все клетки, в которых уже стоит X или O.
        count_fill_cells = 0

        # i — индекс строки, j — индекс столбца.
        for i in range(COUNT_CELLS):
            for j in range(COUNT_CELLS):
                if field[i][j] != EMPTY_SIGN:
                    count_fill_cells += 1

        # Всего на поле COUNT_CELLS * COUNT_CELLS, то есть 9 клеток.
        # Если заняты все клетки и победителя выше не нашли, это ничья.
        if count_fill_cells == COUNT_CELLS * COUNT_CELLS:
            return "Ничья"

    # Если победителя нет и хотя бы одна клетка свободна,
    # возвращаем специальное значение: партия ещё продолжается.
    return "none"


# -----------------------------
# ГЛАВНЫЙ ЦИКЛ ИГРЫ
# -----------------------------

# Один проход цикла соответствует одному кадру.
# На каждом кадре программа обрабатывает события, обновляет состояние
# игры, заново рисует все элементы и показывает готовый кадр.
while is_run == True:
    # pygame.event.get() забирает из очереди все события,
    # накопившиеся с момента предыдущего кадра.
    for event in pygame.event.get():
        # Событие QUIT возникает при нажатии на кнопку закрытия окна.
        if event.type == pygame.QUIT:
            is_run = False

        # MOUSEBUTTONDOWN означает нажатие любой кнопки мыши.
        if event.type == pygame.MOUSEBUTTONDOWN:
            # event.button == 1 — это левая кнопка мыши.
            # Ход принимается только пока текущая партия не закончена.
            if event.button == 1 and is_run_current_game == True:
                # Получаем положение курсора относительно левого верхнего угла окна.
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Проверяем, находится ли точка нажатия внутри поля.
                # Правая и нижняя границы не включаются, поэтому используется <:
                # на самой границе уже получился бы несуществующий индекс 3.
                if (
                    mouse_x >= FIELD_X
                    and mouse_x < FIELD_X + FIELD_SIZE
                    and mouse_y >= FIELD_Y
                    and mouse_y < FIELD_Y + FIELD_SIZE
                ):
                    # Вычитаем координаты начала поля и получаем положение
                    # курсора уже относительно самого игрового поля.
                    normalized_mouse_x = mouse_x - FIELD_X
                    normalized_mouse_y = mouse_y - FIELD_Y

                    # Делим координаты на размер клетки без остатка.
                    # Например, Y от 0 до 199 даёт строку 0,
                    # от 200 до 399 — строку 1, от 400 до 599 — строку 2.
                    # По вертикали получаем строку i, по горизонтали — столбец j.
                    i = normalized_mouse_y // CELL_SIZE
                    j = normalized_mouse_x // CELL_SIZE

                    # Если клетка уже занята, программа ничего не делает
                    # и право хода остаётся у того же игрока.
                    if field[i][j] == EMPTY_SIGN:
                        # Записываем знак текущего игрока в выбранную клетку.
                        field[i][j] = current_player

                        # Проверять результат нужно сразу после успешного хода,
                        # потому что этот ход мог стать победным или заполнить поле.
                        winner = check_winner()

                        if winner != "none":
                            # Останавливаем текущую партию, чтобы после её завершения
                            # нельзя было продолжать ставить знаки на поле.
                            is_run_current_game = False

                            # Показываем результат и выделяем его зелёным цветом.
                            top_text_value = f"Кто победил: {winner}"
                            top_text_color = TEXT_WIN_COLOR

                        # Игрок меняется только в том случае, если партия продолжается.
                        # После победного хода менять current_player уже не требуется.
                        if is_run_current_game == True:
                            if current_player == X_SIGN:
                                current_player = O_SIGN
                            else:
                                current_player = X_SIGN

                            top_text_value = f"Ход игрока: {current_player}"

        # KEYDOWN возникает один раз в момент нажатия клавиши.
        if event.type == pygame.KEYDOWN:
            # K_r соответствует клавише R в английской раскладке.
            if event.key == pygame.K_r:
                # Создаём новое пустое игровое поле.
                field = [
                    [EMPTY_SIGN, EMPTY_SIGN, EMPTY_SIGN],
                    [EMPTY_SIGN, EMPTY_SIGN, EMPTY_SIGN],
                    [EMPTY_SIGN, EMPTY_SIGN, EMPTY_SIGN],
                ]

                # Возвращаем все игровые переменные в начальное состояние:
                # первым снова ходит X, надпись становится обычной,
                # а установка знаков снова разрешается.
                current_player = X_SIGN

                top_text_value = "Ход игрока: X"

                is_run_current_game = True

                top_text_color = TEXT_REGULAR_COLOR

    # -----------------------------
    # ОТРИСОВКА ТЕКУЩЕГО КАДРА
    # -----------------------------

    # Сначала полностью закрашиваем прошлый кадр цветом фона.
    # Благодаря этому на экране не остаются следы старых изображений.
    screen.fill(BACKGROUND_COLOR)

    # Поверх фона рисуем прямоугольник игрового поля.
    # border_radius скругляет его углы.
    pygame.draw.rect(
        screen,
        FIELD_COLOR,
        (FIELD_X, FIELD_Y, FIELD_SIZE, FIELD_SIZE),
        border_radius=15,
    )

    # Для поля 3 на 3 нужны две вертикальные и две горизонтальные линии.
    # line_number последовательно принимает значения 1 и 2.
    for line_number in range(1, 2 + 1):
        # Вертикальная линия смещается вправо на CELL_SIZE * line_number.
        pygame.draw.line(
            screen,
            LINE_COLOR,
            # Начальная точка линии находится сверху.
            (FIELD_X + CELL_SIZE * line_number, FIELD_Y),
            # Конечная точка находится внизу игрового поля.
            (FIELD_X + CELL_SIZE * line_number, FIELD_Y + FIELD_SIZE),
            # Последний аргумент задаёт толщину линии в пикселях.
            6,
        )

        # Горизонтальная линия смещается вниз на CELL_SIZE * line_number.
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (FIELD_X, FIELD_Y + CELL_SIZE * line_number),
            (FIELD_X + FIELD_SIZE, FIELD_Y + CELL_SIZE * line_number),
            6,
        )

    # Перебираем все девять клеток и рисуем содержащиеся в них знаки.
    # Пустые клетки пропускаются и остаются без изображения.
    for i in range(0, COUNT_CELLS):
        for j in range(0, COUNT_CELLS):
            # Вычисляем координаты левого верхнего угла текущей клетки.
            # j влияет на горизонтальную координату X, i — на вертикальную Y.
            cell_x = j * CELL_SIZE + FIELD_X
            cell_y = i * CELL_SIZE + FIELD_Y

            # Крестик состоит из двух диагональных линий.
            # X_MARGIN оставляет одинаковый отступ от всех краёв клетки.
            if field[i][j] == X_SIGN:
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (cell_x + X_MARGIN, cell_y + X_MARGIN),
                    (cell_x + CELL_SIZE - X_MARGIN, cell_y + CELL_SIZE - X_MARGIN),
                    X_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (cell_x + CELL_SIZE - X_MARGIN, cell_y + X_MARGIN),
                    (cell_x + X_MARGIN, cell_y + CELL_SIZE - X_MARGIN),
                    X_WIDTH,
                )

            # Нолик рисуется окружностью, центр которой находится
            # ровно посередине текущей клетки.
            elif field[i][j] == O_SIGN:
                pygame.draw.circle(
                    screen,
                    O_COLOR,
                    (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2),
                    O_RADIUS,
                    O_WIDTH,
                )

    # Метод render превращает строку в отдельную поверхность с текстом.
    # Второй аргумент True включает сглаживание краёв символов.
    top_text = top_font.render(
        top_text_value,
        True,
        top_text_color,
    )

    # Создаём прямоугольник текста и размещаем его центр
    # по центру свободной области над игровым полем.
    top_text_rect = top_text.get_rect(center=(SCREEN_WIDTH // 2, VERTICAL_MARGIN // 2))

    # Копируем подготовленную поверхность с текстом на основную поверхность окна.
    screen.blit(top_text, top_text_rect)

    # Аналогично подготавливаем нижнюю подсказку о перезапуске игры.
    bottom_text = bottom_font.render(
        bottom_text_value,
        True,
        TEXT_REGULAR_COLOR,
    )

    # Размещаем её по центру свободной области под игровым полем.
    bottom_text_rect = bottom_text.get_rect(
        center=(SCREEN_WIDTH // 2, VERTICAL_MARGIN + FIELD_SIZE + VERTICAL_MARGIN // 2)
    )

    screen.blit(bottom_text, bottom_text_rect)

    # Пока выполнялась отрисовка, изменения существовали в памяти.
    # flip() показывает пользователю полностью готовый кадр целиком.
    pygame.display.flip()

    # Если кадр был рассчитан слишком быстро, tick() сделает небольшую паузу.
    # В результате главный цикл выполняется не чаще 60 раз в секунду.
    clock.tick(60)

# Когда is_run становится False, цикл завершается.
# pygame.quit() освобождает ресурсы pygame и корректно закрывает его модули.
pygame.quit()
