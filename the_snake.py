from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, body_color=WHITE):
        self.body_color = body_color
        self.position = None
    
    def draw(self):
        """
        Отрисовка фигур с переопределением в наследуемых классах.
        """
        pass


class Apple(GameObject):
    """
    Яблоко, появляющееся в случайной ячейке игрового поля.
    Наследует от GameObject.
    """
    def __init__(self, color=APPLE_COLOR):
        super().__init__(body_color)
        self._body_color = color
        self._randomize_position()

    def randomize_position(self):
        max_x_cells = SCREEN_WIDTH // GRID_SIZE
        max_y_cells = SCREEN_HEIGHT // GRID_SIZE
        x_index = random.randint(0, max_x_cells - 1)
        y_index = random.randint(0, max_y_cells - 1)
        self.position = (x_index * GRID_SIZE, y_index * GRID_SIZE)     
    def draw(self, screen):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, color=SNAKE_COLOR):
        super().__init__(self, body_color)
        self._reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self._positions[0]

    def move(self, screen_width, screen_height):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя последний
        элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self._direction
        new_head = (
            (head_x + dx * GRID_SIZE) % screen_width,
            (head_y + dy * GRID_SIZE) % screen_height,
        )
        self._positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self._last = self._positions.pop()
        else:
            self._last = None

    def update_direction(self):
        """Обновляет текущее направление движения змейки."""
        if self._next_direction:
            curr_dx, curr_dy = self._direction
            next_dx, next_dy = self._next_direction

            if curr_dx + next_dx != 0 or curr_dy + next_dy != 0:
                self._direction = self._next_direction

        self._next_direction = None


    def reset(self):
        self._length = 1
        self._positions = [self.position]
        self._direction = RIGHT
        self._next_direction = None
        self._last = None

    def draw(self, screen):
        """Отрисовывает змейку на экране, затирая след."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                

def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    apple.draw(screen)
    while True:
        clock.tick(SPEED)
  
        # Тут опишите основную логику игры.
        # handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            apple.draw(screen)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw(screen)
        pygame.display.update()
        snake.draw(screen)


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
