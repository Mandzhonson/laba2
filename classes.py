import random


class Player:
    __hits: list
    __defeat_flag: bool
    __ships: list
    AI: bool
    __count_plain: int

    def __init__(self, AI: bool = False) -> None:
        self.__hits = [[False for _ in range(10)] for _ in range(10)]
        self.__defeat_flag = False
        self.AI = AI
        self.__ships = [[False for _ in range(10)] for _ in range(10)]
        self.__count_plain = 0

    def get_hits(self) -> list:
        return self.__hits

    def get_ships(self) -> list[bool]:
        return self.__ships

    def get_flag(self) -> bool:
        return self.__defeat_flag

    def get_count(self) -> int:
        return self.__count_plain

    def set_AI(self, AI):
        self.AI = AI

    def set_clear_ship(self) -> None:
        #когда очищаем поле, очищаем все корабли у игрока
        self.__count_plain = 0
        self.__ships = [[False for _ in range(10)] for _ in range(10)]

    def place_random_ships(self) -> None:
        #рандомная расстановка кораблей на поле(для ИИ)
        ships_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        random.shuffle(ships_sizes)

        for size in ships_sizes:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                x = random.randint(0, 9)
                y = random.randint(0, 9)

                if self.can_place_ship(x, y, size, orientation):
                    self.place_ship(x, y, size, orientation)
                    placed = True

    def place_ship(self, row: int, col: int, ship_length: int = 1, orientation: str = 'horizontal') -> None:
        #расстановка кораблей вручную
        if orientation == 'horizontal':
            for i in range(ship_length):
                self.__ships[row][col + i] = True
            self.__count_plain += 1
        elif orientation == 'vertical':
            for i in range(ship_length):
                self.__ships[row + i][col] = True
            self.__count_plain += 1

    def delete_ship(self, row: int, col: int, ship_length: int, orientation: str = 'horizontal') -> None:
        #отмена последнего действия и соотвественно удаление корабля с поля
        if orientation == "horizontal":
            for i in range(ship_length):
                self.__ships[row][col + i] = False
        elif orientation == 'vertical':
            for i in range(ship_length):
                self.__ships[row + i][col] = False
        self.__count_plain -= 1

    def can_place_ship(self, row: int, col: int, size: int, orientation: str) -> bool:
        #проверка на возможность постановки корабля
        if orientation == 'horizontal' and col + size > 10:
            return False
        if orientation == 'vertical' and row + size > 10:
            return False

        for i in range(size):
            ship_row = row if orientation == 'horizontal' else row + i
            ship_col = col if orientation == 'vertical' else col + i
            if self.__ships[ship_row][ship_col]:
                return False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    adj_row, adj_col = ship_row + dr, ship_col + dc
                    if 0 <= adj_row < 10 and 0 <= adj_col < 10:
                        if self.__ships[adj_row][adj_col]:
                            return False
        return True

    def make_shot(self, row: int, col: int) -> bool:
        #выстрел
        if self.__hits[row][col]:
            return False

        self.__hits[row][col] = True
        if self.__ships[row][col]:
            self.__ships[row][col] = False
            self.__count_plain -= 1
            if self.__count_plain == 0:
                self.__defeat_flag = True
            return True
        return False

    def is_ship_sunk(self, ship_cells: list) -> bool:
        #проверка на утопленный корабль
        for x, y in ship_cells:
            if not self.get_hits()[x][y]:
                return False
        return True

    def all_ships_sunk(self) -> bool:
        #проверка:уничтожены ли все корабли
        for row in range(10):
            for col in range(10):
                if self.__ships[row][col] and not self.__hits[row][col]:
                    return False
        return True

    def get_surrounding(self, x: int, y: int) -> list:
        #вычисление координат вокруг корабля
        surrounding_cells = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    surrounding_cells.append((nx, ny))
        return surrounding_cells

    def get_ship_cells(self, x: int, y: int) -> list:
        #вычисление координат, которые присуще кораблю
        ship_cells = [(x, y)]
        ny = y - 1
        while ny >= 0 and self.__ships[x][ny]:
            ship_cells.append((x, ny))
            ny -= 1

        ny = y + 1
        while ny < 10 and self.__ships[x][ny]:
            ship_cells.append((x, ny))
            ny += 1

        nx = x - 1
        while nx >= 0 and self.__ships[nx][y]:
            ship_cells.append((nx, y))
            nx -= 1

        nx = x + 1
        while nx < 10 and self.__ships[nx][y]:
            ship_cells.append((nx, y))
            nx += 1

        return ship_cells
