import tkinter
from tkinter import *
from tkinter.messagebox import showinfo, askyesno


class Application:
    master: Tk
    canvas: Canvas
    def draw_empty_field(self):
        self.canvas.bind_all("<Button-1>",self.left_click)
        step_x = (self.width//2) // 10
        step_y = (self.height//2) // 10
        step = min(step_x,step_y)
        for i in range(11):
            x = i * step
            self.canvas.create_line(x+2*step, step*2, x+2*step, step*12, fill="blue")
            self.canvas.create_line(x+20*step, step*2, x+20*step, step*12, fill="blue")
        for i in range(11):
            y = i * step
            self.canvas.create_line(step*2, y+2*step,step*12, y+2*step,fill="blue")
            self.canvas.create_line(step*20, y+2*step,x+20*step, y+2*step,fill="blue")
        alph = "АБВГДЕЖЗИКЛ"
        
        for i in range(10):
            self.canvas.create_text(step, step * 2 + i * step + step // 2, text=str(i + 1), anchor="w",font="Arial",fill="Blue")
            self.canvas.create_text(19*step, step * 2 + i * step + step // 2, text=str(i + 1), anchor="w",font="Arial",fill="Blue")
            self.canvas.create_text(step * 2 + i * step + step // 2, step*2-10, text=alph[i],font="Arial",fill="Blue")
            self.canvas.create_text(step * 20 + i * step + step // 2, step*2-10, text=alph[i],font="Arial",fill="Blue")
    def left_click(self,event):
        pass
    def click_exit(self) -> None:
            # Операция закрытия приложения через меню
        result = askyesno(title="Подтверждение выхода",
                      message="Вы уверены, что хотите выйти?")
        if result:
            self.master.destroy()
        else:
            showinfo("Отмена операции", "Операция выхода отменена.")

    def rules(self):
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

    def create_menu(self):
        # создание меню
        main_menu = Menu(self.master)
        new_game_menu = Menu(tearoff=0)
        new_game_menu.add_command(label="1 player")
        new_game_menu.add_command(label="2 players")
        setting_menu = Menu(tearoff=0)
        

        screen_resol_menu = Menu(setting_menu, tearoff=0)
        screen_resol_menu.add_command(
            label="1280x720", command=lambda: self.create_main(1280,720))
        screen_resol_menu.add_command(
            label="1366x768", command=lambda: self.create_main(1366,768))
        screen_resol_menu.add_command(
            label="1440x900", command=lambda: self.create_main(1440,900))
        screen_resol_menu.add_command(
            label="1600x900", command=lambda: self.create_main(1600,900))
        screen_resol_menu.add_command(
            label="1920x1080", command=lambda: self.create_main(1920,1080))
        screen_resol_menu.add_command(
            label="1920x1200", command=lambda: self.create_main(1920,1200))
        screen_resol_menu.add_command(
            label="2560x1080", command=lambda: self.create_main(2560,1080))
        screen_resol_menu.add_command(
            label="2560x1440", command=lambda: self.create_main(2560,1440))

        setting_menu.add_cascade(
            label="Screen Resolution", menu=screen_resol_menu)
        setting_menu.add_separator()
        setting_menu.add_command(label="Rules", command=self.rules)
        main_menu.add_cascade(label="New game", menu=new_game_menu)
        main_menu.add_cascade(label="Settings", menu=setting_menu)
        main_menu.add_cascade(label="Exit", command=self.click_exit)
        self.master.config(menu=main_menu)

    def create_main(self,width,height):
        self.width = width
        self.height = height
        if self.canvas is not None:
            self.canvas.destroy()
        self.master.geometry(f"{self.width}x{self.height}+0+0")
        self.canvas=Canvas(master=self.master,bg="white",width=self.width,height=self.height)
        self.draw_empty_field()
        self.canvas.pack()


    def __init__(self, master) -> None:
        self.master = master
        self.width = 1280
        self.height = 720
        self.canvas=None
        self.create_main(self.width,self.height)
        self.create_menu()
        self.draw_empty_field()