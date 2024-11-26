class Player:
    __hits: list
    __defeat_flag: bool
    __ships: list
    AI: bool
    __count_plain: int

    def __init__(self, AI=False) -> None:
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

    def place_ship(self, row, col, ship_length=1, orientation='horizontal'):
        if orientation == 'horizontal':
            if col + ship_length <= 10 and col + ship_length > 0:
                for i in range(ship_length):
                    self.__ships[row][col + i] = True
                self.__count_plain += 1
        elif orientation == 'vertical':
            if row + ship_length <= 10 and row + ship_length > 0:
                for i in range(ship_length):
                    self.__ships[row + i][col] = True
                self.__count_plain += 1

    def can_place_ship(self, row, col, size, orientation):
        if orientation == 'horizontal':
            if col + size > 10:
                return False
            for i in range(size):
                if self.ships[row][col + i]:
                    return False
                if col + i - 1 >= 0 and self.ships[row][col + i - 1]:
                    return False
                if col + i + 1 < 10 and self.ships[row][col + i + 1]:
                    return False
            if row - 1 >= 0:
                for i in range(size):
                    if self.ships[row - 1][col + i]:
                        return False
            if row + 1 < 10:
                for i in range(size):
                    if self.ships[row + 1][col + i]:
                        return False
