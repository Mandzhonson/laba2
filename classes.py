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
    def delete_ship(self, row, col, ship_length, orientation='horizontal'):
        if orientation=="horizontal":
            for i in range(ship_length):
                if col + ship_length <= 10 and col + ship_length > 0:
                    self.__ships[row][col+i] = False
            self.__count_plain-=1

        elif orientation == 'vertical':
            for i in range(ship_length):
                if row + ship_length <= 10 and row + ship_length > 0:
                    self.__ships[row+i][col] = False
            self.__count_plain-=1
    
    def can_place_ship(self, row, col, size, orientation):
        if orientation == 'horizontal':
            if col + size > 10:
                return False
        elif orientation == 'vertical':
            if row + size > 10:
                return False
        for i in range(size):
            if orientation == 'horizontal':
                ship_row, ship_col = row, col + i
            elif orientation == 'vertical':
                ship_row, ship_col = row + i, col

            if self.__ships[ship_row][ship_col]:
                return False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    adj_row, adj_col = ship_row + dr, ship_col + dc
                    if 0 <= adj_row < 10 and 0 <= adj_col < 10:
                        if self.__ships[adj_row][adj_col]:
                            return False
        return True
    