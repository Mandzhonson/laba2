from applications import *


root = Tk()
root.title("Морской бой")
app = Application(root)
app.master.protocol("WM_DELETE_WINDOW", app.click_exit)
root.mainloop()
