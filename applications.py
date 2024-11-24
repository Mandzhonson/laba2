import tkinter
from tkinter import *
from tkinter.messagebox import showinfo,askyesno


class Application:
    master: Tk

    def click_exit(self) -> None:
        # Операция закрытия приложения через меню
        result = askyesno(title="Подтверждение выхода",
                          message="Вы уверены, что хотите выйти?")
        if result:
            self.master.destroy()
        else:
            showinfo("Отмена операции", "Операция выхода отменена.")

    def __init__(self, master) -> None:
        self.master = master
        # создание меню
        main_menu = Menu(self.master)
        new_game_menu = Menu(tearoff=0)
        new_game_menu.add_command(label="1 player")
        new_game_menu.add_command(label="2 player")
        setting_menu = Menu(tearoff=0)
        setting_menu.add_command(label="Screen Resolution")
        main_menu.add_cascade(label="New game", menu=new_game_menu)
        main_menu.add_cascade(label="Settings", menu=setting_menu)
        main_menu.add_cascade(label="Exit", command=self.click_exit)
        master.config(menu=main_menu)
        #
