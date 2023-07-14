# Создаем пустое поле 3x3
board = [[' ' for _ in range(3)] for _ in range(3)]

# Функция для отображения поля
def display_board():
    print('---------')
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} ', end='|')
        print('\n---------')

# Функция для проверки выигрышной комбинации
def check_win(player):
    # Проверка по горизонтали и вертикали
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    # Проверка по диагоналям
    if (board[0][0] == board[1][1] == board[2][2] == player) or (board[0][2] == board[1][1] == board[2][0] == player):
        return True

    return False

# Функция для хода игрока
def make_move(player):
    while True:
        try:
            row = int(input('Введите номер строки (0-2): '))
            col = int(input('Введите номер столбца (0-2): '))

            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
 board[row][col] = player
 break
            else:
                print('Некорректный ход. Попробуйте еще раз.')
        except ValueError:
            print('Некорректный ввод. Введите целое число.')

# Основной игровой цикл
def play_game():
    current_player = 'X'

    while True:
        display_board()
        print(f'Ходит игрок {current_player}')

        make_move(current_player)

        if check_win(current_player):
            display_board()
            print(f'Игрок {current_player} победил!')
            break

        # Проверка на ничью
        if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
            display_board()
            print('Ничья!')
            break

        # Смена игрока
        current_player = 'O' if current_player == 'X' else 'X'

# Запуск игры
play_game()
