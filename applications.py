from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno
from classes import Player
from random import randint


class Application:
    master: Tk
    pl1: Player
    pl2: Player
    fl_pl2: bool
    current_player: Player
    enemy_player: Player | None
    field_pl1: Canvas
    field_pl2: Canvas
    btn1: Button
    btn2: Button
    btn_clear: Button | None
    btn_cancel: Button | None
    orientation_var: StringVar
    horizontal_radio: Radiobutton | None
    vertical_radio: Radiobutton | None

    def __init__(self, master):
        self.master = master
        self.master.title("Морской бой")
        self.create_menu()
        self.pl1 = Player()
        self.pl2 = Player(True)
        self.fl_pl2 = False
        self.current_player = self.pl1
        self.field_pl1 = Canvas(
            master=self.master, bg="white", width=550, height=550)
        self.field_pl2 = Canvas(
            master=self.master, bg="white", width=550, height=550)
        self.field_pl1.pack(side=LEFT, padx=10, pady=10)
        self.field_pl2.pack(side=RIGHT, padx=10, pady=10)
        self.draw_field(self.field_pl1, self.pl1)
        self.draw_field(self.field_pl2, self.pl2)
        self.btn1 = Button(self.master, text="1 игрок", command=lambda: (
            self.pl2.set_AI(True), self.start_game()))
        self.btn2 = Button(self.master, text="2 игрока", command=lambda: (
            self.set_fl(True), self.start_game()))
        self.btn_clear = Button(self.master, text="Очистить поле",
                                command=lambda: self.clear_field(self.current_player))
        self.orientation_var = StringVar(value='horizontal')
        self.horizontal_radio = self.vertical_radio = None
        self.btn_cancel = None
        self.btn1.pack()
        self.btn2.pack()

    def click_exit(self) -> None:
        # Операция закрытия приложения через меню
        result = askyesno(title="Подтверждение выхода",
                          message="Вы уверены, что хотите выйти?")
        if result:
            self.master.destroy()
        else:
            showinfo("Отмена операции", "Операция выхода отменена.")

    def set_fl(self, fl: bool) -> None:
        self.fl_pl2 = fl

    def draw_field(self, canvas: Tk, player: Player) -> None:
        #рисуем поле,исходя из массива кораблей игрока(если есть,то рисуем и корабль)
        cell_size = 50
        for row in range(10):
            for col in range(10):
                x1 = col * cell_size + cell_size
                y1 = row * cell_size + cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                if player.get_ships()[row][col]:
                    canvas.create_rectangle(
                        x1, y1, x2, y2, fill="Gray", outline="Grey")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="Blue")

        alph = "АБВГДЕЖЗИК"
        for i in range(10):
            canvas.create_text((i + 1) * cell_size + cell_size //
                               2, cell_size // 2, text=alph[i])
            canvas.create_text(cell_size // 2, (i + 1) *
                               cell_size + cell_size // 2, text=str(i + 1))

    def draw_field_empty(self, canvas: Canvas) -> None:
        #рисовка просто пустого поля
        cell_size = 50
        for row in range(10):
            for col in range(10):
                x1 = col * cell_size + cell_size
                y1 = row * cell_size + cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, outline="Blue")

        alph = "АБВГДЕЖЗИК"
        for i in range(10):
            canvas.create_text((i + 1) * cell_size + cell_size //
                               2, cell_size // 2, text=alph[i])
            canvas.create_text(cell_size // 2, (i + 1) *
                               cell_size + cell_size // 2, text=str(i + 1))

    def click_mouse(self, event) -> None:
        #обработка нажатия ЛКМ(расстановка кораблей)
        canvas = self.field_pl1 if self.current_player == self.pl1 else self.field_pl2
        y = event.x // 50 - 1
        x = event.y // 50 - 1
        size = None
        if 0 <= x < 10 and 0 <= y < 10:
            if self.current_player.get_count() < 4:
                size = 1
            elif self.current_player.get_count() < 7:
                size = 2
            elif self.current_player.get_count() < 9:
                size = 3
            elif self.current_player.get_count() == 9:
                size = 4
            else:
                return

            if size:
                if self.horizontal_radio is None and self.vertical_radio is None:
                    self.horizontal_radio = Radiobutton(
                        self.master, text="Горизонтально", variable=self.orientation_var, value='horizontal')
                    self.horizontal_radio.pack()
                    self.vertical_radio = Radiobutton(
                        self.master, text="Вертикально", variable=self.orientation_var, value='vertical')
                    self.vertical_radio.pack()

                orientation = self.orientation_var.get()
                if self.current_player.can_place_ship(x, y, size, orientation):
                    self.current_player.place_ship(x, y, size, orientation)
                    self.draw_field(canvas, self.current_player)
                    if self.btn_cancel is not None:
                        self.btn_cancel.destroy()

                    self.btn_cancel = Button(
                        master=self.master,
                        text="Отмена действия",
                        command=lambda: self.cancel_plain(
                            x, y, size, orientation, canvas)
                    )
                    self.btn_cancel.pack()
                else:
                    self.btn_cancel.destroy()
                    showerror(
                        title="Ошибка", message="Нельзя расположить корабли на данных клетках")
                if self.current_player.get_count() == 10:
                    if self.fl_pl2 and self.current_player == self.pl1:
                        self.btn_cancel.destroy()
                        self.horizontal_radio.destroy()
                        self.vertical_radio.destroy()
                        self.horizontal_radio = self.vertical_radio = None
                        self.current_player = self.pl2
                        self.field_pl1.unbind("<Button-1>")
                        self.field_pl2.bind("<Button-1>", self.click_mouse)
                        self.field_pl1.delete("all")
                        showinfo(
                            "Подсказка", "Теперь расставляет корабли игрок 2 на правом поле.")
                    elif not self.fl_pl2 and self.current_player == self.pl1:
                        self.btn_cancel.destroy()
                        self.horizontal_radio.destroy()
                        self.vertical_radio.destroy()
                        self.vertical_radio = self.horizontal_radio = self.btn_cancel = None
                        self.pl2.place_random_ships()
                        self.end_preparation()
                    else:
                        self.end_preparation()

    def clear_field(self, player: Player) -> None:
        #кнопка очистка поля во время расстановки кораблей
        self.btn_cancel.destroy()
        self.btn_cancel = None
        player.set_clear_ship()
        if player == self.pl1:
            self.field_pl1.delete("all")
            self.draw_field_empty(self.field_pl1)
        else:
            self.field_pl2.delete("all")
            self.draw_field_empty(self.field_pl2)

    def end_preparation(self) -> None:
        #завершение расстановки кораблей и начало игры
        self.btn_clear.destroy()
        showinfo("Игра началась",
                 "Оба игрока разместили корабли. Начинаем сражение! Ход за 1 игроком.")
        self.field_pl1.unbind("<Button-1>")
        self.field_pl2.unbind("<Button-1>")
        self.current_player = self.pl1
        self.enemy_player = self.pl2

        if self.fl_pl2:
            self.field_pl2.delete("all")
            self.draw_field_empty(self.field_pl1)
            self.draw_field_empty(self.field_pl2)
            self.btn_cancel.destroy()
            self.vertical_radio.destroy()
            self.horizontal_radio.destroy()
            self.field_pl2.bind("<Button-1>", self.game)
        else:
            self.field_pl2.bind("<Button-1>", self.game)
        showinfo("Ход", "Ход игрока 1.")

    def cancel_plain(self, x: int, y: int, size: int, orientation: str, canvas: Canvas) -> None:
        #отмена последнего действия
        self.current_player.delete_ship(x, y, size, orientation)
        canvas.delete("all")
        self.draw_field(canvas, self.current_player)
        if self.btn_cancel is not None:
            self.btn_cancel.destroy()

    def start_game(self, flag: bool = True) -> None:
        #запуск приложения и нажатия одной из кнопки(1 игрок/2 игрока)
        showinfo("Подсказка", "Разместите корабли. Управление:\nЛКМ - постановка корабля\nКнопка \"Отмена действия\" - удаляет последний поставленный корабль")
        self.field_pl1.bind("<Button-1>", self.click_mouse)
        if flag:
            self.btn1.destroy()
            self.btn2.destroy()
            self.btn_clear.pack()
        else:
            self.btn1.destroy()
            self.btn2.destroy()
            self.pl1.set_clear_ship()
            self.pl2.set_clear_ship()
            self.btn_clear = Button(self.master, text="Очистить поле",
                                    command=lambda: self.clear_field(self.current_player))
            self.field_pl1.delete("all")
            self.field_pl2.delete("all")
            self.draw_field_empty(self.field_pl1)
            self.draw_field_empty(self.field_pl2)
            self.btn_clear.pack()

    def game(self, event) -> None:
        #логика игры
        canvas = self.field_pl2 if self.current_player == self.pl1 else self.field_pl1
        enemy_player = self.pl2 if self.current_player == self.pl1 else self.pl1
        y = event.x // 50 - 1
        x = event.y // 50 - 1

        if 0 <= x < 10 and 0 <= y < 10:
            if enemy_player.get_hits()[x][y]:
                showerror("Ошибка", "Вы уже стреляли сюда!")
                return

            hit = enemy_player.make_shot(x, y)
            self.draw_hit(canvas, x, y, hit)

            if hit:
                ship_cells = enemy_player.get_ship_cells(x, y)
                if enemy_player.is_ship_sunk(ship_cells):
                    self.mark_surrounding(enemy_player, canvas, ship_cells)
                if enemy_player.all_ships_sunk():
                    showinfo("Конец игры", f"Победил {
                             ('Игрок 1' if self.current_player == self.pl1 else 'Игрок 2')}!")
                    return
                return
        else:
            showerror("Ошибка", "Вы вышли за пределы поля")
            return

        if not self.fl_pl2:
            self.ai_move()
        else:
            self.switch_player()

    def ai_move(self) -> None:
        #ход ИИ
        while True:
            x, y = randint(0, 9), randint(0, 9)
            if not self.pl1.get_hits()[x][y]:
                hit = self.pl1.make_shot(x, y)
                self.draw_hit(self.field_pl1, x, y, hit)

                if hit:
                    ship_cells = self.pl1.get_ship_cells(x, y)
                    if self.pl1.is_ship_sunk(ship_cells):
                        self.mark_surrounding(
                            self.pl1, self.field_pl1, ship_cells)
                    if self.pl1.all_ships_sunk():
                        showinfo("Конец игры", "ИИ победил!")
                    continue

                break

    def mark_surrounding(self, player: Player, canvas: Canvas, ship_cells: list) -> None:
        #Если корабль уничтожен, закрашиваем поля вокруг(работает не совсем корректно)
        marked_cells = set()

        for x, y in ship_cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        if (nx, ny) not in ship_cells and (nx, ny) not in marked_cells:
                            if not player.get_hits()[nx][ny]:
                                player.get_hits()[nx][ny] = True
                                marked_cells.add((nx, ny))
                                canvas.create_oval(
                                    ny * 50 + 50 + 10, nx * 50 + 50 + 10,
                                    (ny + 1) * 50 + 50 -
                                    10, (nx + 1) * 50 + 50 - 10,
                                    outline='blue', fill='blue'
                                )

    def switch_player(self) -> None:
        #смена хода
        if self.current_player == self.pl1:
            self.current_player = self.pl2
            self.enemy_player = self.pl1
            showinfo("Ход", "Ход игрока 2.")
            self.field_pl1.unbind("<Button-1>")
            self.field_pl2.unbind("<Button-1>")
            self.field_pl1.bind("<Button-1>", self.game)
        else:
            self.current_player = self.pl1
            self.enemy_player = self.pl2
            showinfo("Ход", "Ход игрока 1.")
            self.field_pl1.unbind("<Button-1>")
            self.field_pl2.unbind("<Button-1>")
            self.field_pl2.bind("<Button-1>", self.game)

    def draw_hit(self, canvas, x, y, hit=True):
        #рисовка попаданий
        cell_size = 50
        x1 = y * cell_size + cell_size
        y1 = x * cell_size + cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        if hit:
            canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
            canvas.create_line(x1, y2, x2, y1, fill="red", width=2)
        else:
            canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="blue")

    def create_menu(self) -> None:
        #создание менюшки
        main_menu = Menu(self.master)
        new_game_menu = Menu(tearoff=0)
        new_game_menu.add_command(label="1 player", command=lambda: (
            self.pl2.set_AI(True), self.start_game(False)))
        new_game_menu.add_command(label="2 players", command=lambda: (
            self.set_fl(True), self.start_game(False)))
        setting_menu = Menu(tearoff=0)

        screen_resol_menu = Menu(setting_menu, tearoff=0)
        screen_resol_menu.add_command(
            label="1280x720", command=lambda: self.master.geometry("1280x720+0+0"))
        screen_resol_menu.add_command(
            label="1366x768", command=lambda: self.master.geometry("1366x768+0+0"))
        screen_resol_menu.add_command(
            label="1440x900", command=lambda: self.master.geometry("1440x900+0+0"))
        screen_resol_menu.add_command(
            label="1600x900", command=lambda: self.master.geometry("1600x900+0+0"))
        screen_resol_menu.add_command(
            label="1920x1080", command=lambda: self.master.geometry("1920x1080+0+0"))
        screen_resol_menu.add_command(
            label="1920x1200", command=lambda: self.master.geometry("1920x1200+0+0"))
        screen_resol_menu.add_command(
            label="2560x1080", command=lambda: self.master.geometry("2560x1080+0+0"))
        screen_resol_menu.add_command(
            label="2560x1440", command=lambda: self.master.geometry("2560x1440+0+0"))

        setting_menu.add_cascade(
            label="Screen Resolution", menu=screen_resol_menu)
        setting_menu.add_separator()
        setting_menu.add_command(label="Rules", command=self.rules)
        main_menu.add_cascade(label="New game", menu=new_game_menu)
        main_menu.add_cascade(label="Settings", menu=setting_menu)
        main_menu.add_cascade(label="Exit", command=self.click_exit)
        self.master.config(menu=main_menu)

    def rules(self) -> None:
        # окно с правилами игры
        rul = Tk()
        rul.title("Правила игры")
        rule_text0 = "«Морской бой» — игра для двух участников, в которой игроки по очереди называют, сообщают иным способом, координаты на карте соперник. Если у врага с этими координатами имеется «корабль», то корабль или его палуба (дека) убивается, попавший делает еще один ход. Цель игрока: первым убить все «корабли» противника."
        rule_text1 = "\n\nПРАВИЛА ИГРЫ:\nИгровое поле — обычно квадрат 10×10 у каждого игрока, на котором размещается флот кораблей. Горизонтали обычно нумеруются сверху вниз, а вертикали помечаются буквами слева направо. При этом используются буквы русского алфавита от «а» до «к» (буквы «ё» и «й» обычно пропускаются) либо от «а» до «и» (с использованием буквы «ё»), либо буквы латинского алфавита от «a» до «j». Иногда используется слово «республика» или «снегурочка», так как в этих 10-буквенных словах ни одна буква не повторяется. Поскольку существуют различные варианты задания системы координат, то об этом лучше заранее договориться."
        rule_text2 = "\nРазмещаются:\n1 корабль — ряд из 4 клеток («четырёхпалубный»; линкор)\n2 корабля — ряд из 3 клеток («трёхпалубные»; крейсера)\n3 корабля — ряд из 2 клеток («двухпалубные»; эсминцы)\n4 корабля — 1 клетка («однопалубные»; торпедные катера)"
        rule_text3 = "\nПри размещении корабли не могут касаться друг друга сторонами и углами. Встречаются, однако, варианты, когда касание углами не запрещается. Встречаются также варианты игры, когда корабли могут размещаться буквой «Г» («трёх-» и «четырёхпалубные»), квадратом или зигзагом («четырёхпалубные»). Кроме того, есть варианты с другим набором кораблей (напр., один пятипалубный, два четырёхпалубных и т. д.) и/или другой формой поля (15×15 для пятипалубных (авианосец))."
        rule_text4 = "Рядом со «своим» полем чертится «чужое» такого же размера, только пустое. Это участок моря, где плавают корабли противника.\nПри попадании в корабль противника — на чужом поле ставится крестик, при холостом выстреле — точка. Попавший стреляет ещё раз."
        rule_text = rule_text0+rule_text1+rule_text2+rule_text3+rule_text4
        rul.geometry("900x400")
        label2 = Label(master=rul, text=rule_text,
                       wraplength=800, justify="left")
        label2.grid(padx=10, pady=10)
        btn = Button(master=rul, text="Ok", command=lambda: rul.destroy(
        ), width=15, height=3, justify="center")
        btn.grid()
        rul.mainloop()
