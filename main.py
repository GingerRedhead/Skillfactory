import random


class BoardOutException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.live = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o:
                cur_x += i
            else:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        board = ""
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                if i == 0:
                    if j == 0:
                        board += "  |"
                    else:
                        board += f" {j} |"
                else:
                    if j == 0:
                        board += f" {i} |"
                    else:
                        board += f" {self.field[i-1][j-1]} |"
            board += "\n"
            board += "-" * (self.size * 4 + 3)
            board += "\n"

        return board

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dot in ship.dots:
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not self.out(cur) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardOutException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        for ship in self.ships:
            if dot in ship.dots:
                ship.live -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.live == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.field[dot.x][dot.y] = "T"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardOutException:
                print("Вы выстрелили за пределы поля!")
            except Exception as e:
                print(e)


class AI(Player):
    def ask(self):
        while True:
            dot = Dot(random.randint(0, 5), random.randint(0, 5))
            print(f"Ход компьютера: {dot.x + 1}, {dot.y + 1}")
            if not self.board.out(dot):
                return dot


class User(Player):
    def ask(self):
        while True:
            coords = input("Ваш ход (введите координаты через пробел): ").split()

            if len(coords) != 2:
                print("Введите две координаты!")
                continue

            x, y = coords

            if not (x.isdigit() and y.isdigit()):
                print("Введите числовые значения!")
                continue

            x = int(x)
            y = int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        self.ai = AI(Board(), Board(hid=True))
        self.us = User(Board(), Board())

    def greet(self):
        print("---------------------")
        print("  Добро пожаловать  ")
        print("    в игру Морской бой    ")
        print("---------------------")
        print("  Формат ввода: x y  ")
        print("  x - номер строки  ")
        print("  y - номер столбца ")

    def random_board(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        random.shuffle(ships)
        for ship in ships:
            while True:
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                o = random.randint(0, 1)
                if o == 0:
                    o = False
                else:
                    o = True
                new_ship = Ship(Dot(x, y), ship, o)

                try:
                    self.ai.board.add_ship(new_ship)
                    break
                except BoardOutException:
                    continue

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board if not self.ai.board.hid else self.ai.enemy_board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь:")
                repeat = self.us.move()
                if repeat:
                    continue
                if self.ai.board.count == 7:
                    print("Вы выиграли!")
                    break
            else:
                print("Ходит компьютер:")
                repeat = self.ai.move()
                if repeat:
                    continue
                if self.us.board.count == 7:
                    print("Компьютер выиграл!")
                    break
            num += 1

    def start(self):
        self.greet()
        self.random_board()
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()
