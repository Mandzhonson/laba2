from tkinter import *
from tkinter.messagebox import showinfo, askyesno
from classes import Player

class Application:
    master: Tk
    def __init__(self,master):
        self.master = master
        self.pl1 = Player()
        self.pl2 = Player(True)
        self.current_player = self.pl1
        self.field_pl1 = Canvas(bg="white",master=self.master,width=550,height=550)
        self.field_pl2 = Canvas(bg="white",master=self.master,width=550,height=550)
        self.field_pl1.pack(side= LEFT,padx=10,pady=10)
        self.field_pl2.pack(side=RIGHT,padx=10,pady=10)
        self.draw_field(self.field_pl1, self.pl1)
        self.draw_field(self.field_pl2, self.pl2)
        self.btn1=Button(text="1 игрок",command=lambda: self.start_game())
        self.btn2=Button(text="2 игрока",command=lambda:self.start_game(True))
        self.btn1.pack()
        self.btn2.pack()
    def draw_field(self,canvas:Tk,player:Player):
        cell_size = 50
        for row in range(10):
            for col in range(10):
                x1 = col * cell_size + cell_size
                y1 = row * cell_size + cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if player.get_ships()[row][col]:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="Gray", outline="Grey")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="Blue")

        alph = "АБВГДЕЖЗИК"
        for i in range(10):
            canvas.create_text((i + 1) * cell_size + cell_size // 2, cell_size // 2, text=alph[i])
            canvas.create_text(cell_size // 2, (i + 1) * cell_size + cell_size // 2, text=str(i + 1))
    def click_mouse(self,event):
        y = event.x//50 - 1
        x = event.y//50 - 1
        if 0 <= x < 10 and 0 <= y < 10:
            if self.current_player.get_count()<4:
                self.current_player.place_ship(x,y,1)
                self.draw_field(self.field_pl1, self.current_player)
            elif self.current_player.get_count()>=4 and self.current_player.get_count()<7:
                self.current_player.place_ship(x,y,2)
                self.draw_field(self.field_pl1, self.current_player)
            elif self.current_player.get_count()>=7 and self.current_player.get_count()<9:
                self.current_player.place_ship(x,y,3)
                self.draw_field(self.field_pl1, self.current_player)
            elif self.current_player.get_count()==9:
                self.current_player.place_ship(x,y,4)
                self.draw_field(self.field_pl1, self.current_player)
            else:   
                print("10 plains on field")
    def start_game(self,pl2=False):
        showinfo("Подсказка","Разместите корабли на поле слева. Управление:\nЛКМ - примерное расположение корабля\nПКМ - подтверждение местоположения")
        if not pl2:
            count = 0
            self.field_pl1.bind("<Button-1>",self.click_mouse)
            while count!=20:
                if count!=4:
                    count+=1
                elif count!=10:
                    count+=2
                elif count!=16:
                    count+=3
                else:
                    count+=4
        else:
            pass