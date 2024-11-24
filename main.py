from applications import *


root = Tk()
root.title("Морской бой")
root.minsize(800,600)
root.maxsize(2560,1440)
root.geometry("800x600+800+100")

app = Application(root)
app.master.protocol("WM_DELETE_WINDOW",app.click_exit) # обработка нажатия кнопки закрытия
root.mainloop()