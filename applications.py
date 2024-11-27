from tkinter import *
from tkinter.messagebox import showinfo, showerror
from classes import Player


class Application:
    master: Tk

    def __init__(self, master):
        self.master = master
        self.pl1 = Player()
        self.pl2 = Player(True)
        self.fl_pl2 = False
        self.current_player = self.pl1
        self.field_pl1 = Canvas(
            bg="white", master=self.master, width=550, height=550)
        self.field_pl2 = Canvas(
            bg="white", master=self.master, width=550, height=550)
        self.field_pl1.pack(side=LEFT, padx=10, pady=10)
        self.field_pl2.pack(side=RIGHT, padx=10, pady=10)
        self.draw_field(self.field_pl1, self.pl1)
        self.draw_field(self.field_pl2, self.pl2)
        self.btn1 = Button(text="1 игрок", command=lambda: (self.pl2.set_AI(True),self.start_game()))
        self.btn2 = Button(text="2 игрока", command= lambda: (self.set_fl(True), self.start_game()))
        self.orientation_var = StringVar(value='horizontal')
        self.horizontal_radio = self.vertical_radio = None
        self.btn_cancel = None
        self.btn1.pack()
        self.btn2.pack()
    def set_fl(self,fl):
        self.fl_pl2=fl
    def draw_field(self, canvas: Tk, player: Player):
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
    def draw_field_empty(self,canvas):
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
    def click_mouse(self, event):
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
                        command=lambda: self.cancel_plain(x, y, size, orientation,canvas)
                    )
                    self.btn_cancel.pack()
                else:
                    self.btn_cancel.destroy()
                    showerror(title="Ошибка", message="Нельзя расположить корабли на данных клетках")
                if self.current_player.get_count() == 10:
                    if self.fl_pl2 and self.current_player == self.pl1:
                        self.btn_cancel.destroy()
                        self.horizontal_radio.destroy()
                        self.vertical_radio.destroy()
                        self.horizontal_radio=self.vertical_radio=None
                        self.switch_player()
                    elif not self.fl_pl2 and self.current_player == self.pl1:
                        self.btn_cancel.destroy()
                        self.horizontal_radio.destroy()
                        self.vertical_radio.destroy()
                        self.pl2.place_random_ships()
                        self.end_preparation()
                    else:
                        self.end_preparation()

    def end_preparation(self):
        showinfo("Игра началась", "Оба игрока разместили корабли. Начинаем сражение! Ход за 1 игроком")
        self.field_pl1.unbind("<Button-1>")
        self.field_pl2.unbind("<Button-1>")
        self.current_player=self.pl1
        if self.fl_pl2:
            self.field_pl2.delete("all")
            self.draw_field_empty(self.field_pl1)
            self.draw_field_empty(self.field_pl2)
            self.btn_cancel.destroy()
            self.vertical_radio.destroy()
            self.horizontal_radio.destroy()
        else:
            print("1 игрок")
    def cancel_plain(self, x, y, size, orientation,canvas):
        self.current_player.delete_ship(x, y, size, orientation)
        canvas.delete("all")
        self.draw_field(canvas, self.current_player)
        if self.btn_cancel is not None:
            self.btn_cancel.destroy()

    def switch_player(self):
        if self.current_player == self.pl1:
            self.current_player = self.pl2
            self.field_pl1.unbind("<Button-1>")
            self.field_pl2.bind("<Button-1>", self.click_mouse)
            self.field_pl1.delete("all")
            showinfo("Подсказка", "Теперь расставляет корабли игрок 2 на правом поле.")
        else:
            self.field_pl2.delete("all")
            self.current_player = self.pl1
            self.field_pl2.unbind("<Button-1>")
            self.field_pl1.bind("<Button-1>", self.click_mouse)
            showinfo("Игра началась", "Оба игрока разместили корабли. Начинаем сражение!")

    def start_game(self):
        showinfo("Подсказка", "Разместите корабли. Управление:\nЛКМ - постановка корабля\nКнопка \"Отмена действия\" - удаляет последний поставленный корабль")
        self.field_pl1.bind("<Button-1>", self.click_mouse)