from tkinter import *
from tkinter import messagebox
import socket
import pickle
from _thread import *
from xoxgame import TicToc
from Hangman import Hangman

class MiniGames(Frame):
    def __init__(self, main_screen):
        Frame.__init__(self, main_screen, padx=30, pady=30)
        # Settings Windows
        self.window = main_screen
        self.width = 600
        self.height = 600
        self.window.wm_iconbitmap('servericon.ico')
        self.window.title("MiniGames")
        self.window.minsize(width=690, height=532)
        self.window.maxsize(width=690, height=532)
        self.window.geometry("690x532+50+50")
        self.window.configure(bg='gray69')
        self.pack()
        # games

        # bg
        self.bg_img = PhotoImage(file="minigamesbg.png")
        self.bg_img_Label = Label(self.window, image=self.bg_img)
        self.bg_img_Label.place(x=0, y=0)

        # Starting
        self.tictoc_image = PhotoImage(file="tictocimage.png")
        self.Label_Tictoc = Label(self.window, text="TicToc", font=("Helvetica", 8), bg='khaki2')
        self.Label_Tictoc.place(x=70, y=270, width=69, height=12)
        self.Button_Tictoc = Button(self.window, image=self.tictoc_image, command=lambda: self.game_play(1))
        self.Button_Tictoc.place(x=70, y=200, width=70, height=70)

        self.hangman_image = PhotoImage(file="hmimg.png")
        self.Label_Hangman = Label(self.window, text="Hangman", font=("Helvetica", 8), bg='khaki2')
        self.Label_Hangman.place(x=170, y=270, width=69, height=12)
        self.Button_Hangman = Button(self.window, image=self.hangman_image, command=lambda: self.game_play(2))
        self.Button_Hangman.place(x=170, y=200, width=70, height=70)

    def game_play(self, n):
        if n == 1:
            start_new_thread(self.tictoc, ())

        if n == 2:
            start_new_thread(self.hangman, ())

    def tictoc(self):
        new_window = Toplevel(self.window)
        TicToc(new_window)

        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()

    def hangman(self):
        new_window = Toplevel(self.window)
        Hangman(new_window)



root = Tk()
app = MiniGames(root)
app.mainloop()
