from tkinter import *
from tkinter import messagebox
import socket
from _thread import *
from tkservertictoc import Server
from tictok import TicToc_Multiplayer
from xoxvscomputer import TicToc_Computer, TicToc_Solo
import pickle
from gametictoc import Game
class TicToc(Frame):
    def __init__(self, main_screen):
        Frame.__init__(self, main_screen, padx=30, pady=30)

        self.window = main_screen
        self.width = 600
        self.height = 600
        self.window.wm_iconbitmap('servericon.ico')
        self.window.title("TicToc")
        self.window.minsize(width=440, height=565)
        self.window.maxsize(width=440, height=565)
        self.window.geometry("440x565+50+50")
        self.window.configure(bg='cyan3')
        self.pack()

        # bg
        self.bg_img = PhotoImage(file="TTBG.png")
        self.bg_img_Label = Label(self.window, image=self.bg_img)
        self.bg_img_Label.place(x=0, y=0)

        # server

        self.server = None
        self.port = None
        self.port_var = StringVar()
        self.port_Label = None
        self.port_entry = None
        self.start_Button = None

        # player
        self.player = None  # 0 = X ,  1 = 0
        self.played_list = []

        # tictoc brand
        self.Button_1 = None
        self.Button_2 = None
        self.Button_3 = None
        self.Button_4 = None
        self.Button_5 = None
        self.Button_6 = None
        self.Button_7 = None
        self.Button_8 = None
        self.Button_9 = None

        # multiplayer, solo, vs computer, guide buttons

        self.multiplayer_button = None
        self.solo_button = None
        self.vs_computer_button = None
        self.guide_button = None


        # for multiplayer create game and join game and back button (I will use it everywhere by constantly changing the back button)
        self.create_game_button = None
        self.join_game_button = None
        self.back_button = None

        # for multiplayer join game
        self.ip = StringVar()
        self.ip_label = None
        self.ip_entry = None

        self.play_button = None

        self.starting()

    def starting(self):
        self.bg_img_Label.place(x=0, y=0)
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()
        self.multiplayer_button = Button(self.window, relief=RAISED, text='Multiplayer', bg='salmon',
                                         font=('Mongolian Baiti', 15, 'normal'), command=self.multiplayer)
        self.solo_button = Button(self.window, relief=RAISED, text='Solo', bg='salmon',
                                  font=('Mongolian Baiti', 15, 'normal'), command=self.solo)
        self.vs_computer_button = Button(self.window, relief=RAISED, text='Vs Computer', bg='salmon',
                                         font=('Mongolian Baiti', 15, 'normal'), command=self.vs_computer)
        self.guide_button = Button(self.window, relief=RAISED, text='?', bg='red', font=('Mongolian Baiti', 20, 'bold'),
                                   command=self.guide)

        self.multiplayer_button.place(x=120, y=250, height=25, width=200)
        self.solo_button.place(x=120, y=285, height=25, width=200)
        self.vs_computer_button.place(x=120, y=320, height=25, width=200)
        self.guide_button.place(x=380, y=510, height=40, width=40)

    def create_game(self):
        self.port_var = StringVar()
        self.port_Label = Label(self.window, relief=GROOVE, text='Entry Port', bg='lemon chiffon')
        self.port_Label.place(x=50, y=100, width=100, height=20)
        self.port_entry = Entry(self.window, textvariable=self.port_var, font=('calibre', 10, 'normal'))
        self.port_entry.place(x=150, y=100, width=70, height=20)
        self.start_Button = Button(self.window, text='Start Server', command=self.start_server, bg='orange')
        self.start_Button.place(x=200, y=200, width=80, height=30)
        self.back_button = Button(self.window, relief=RAISED, text='<--', bg='salmon',
                                  font=('Mongolian Baiti', 15, 'normal'))
        self.back_button.configure(command=self.starting)
        self.back_button.place(x=20, y=520, height=20, width=40)

    def start_server(self):
        a = str(self.port_var.get())
        self.server = socket.gethostbyname(socket.gethostname())
        try:
            if int(a) in range(4000, 6000):
                self.start_Button.destroy()
                self.port_Label.destroy()
                self.port_entry.destroy()
                self.port = int(a)
                new_window = Toplevel(self.window)
                new_window_2 = Toplevel(self.window)
                start_new_thread(Server, (new_window, self.port))
                start_new_thread(TicToc_Multiplayer, (new_window_2, self.port, str(self.server)))
            else:
                messagebox.showerror('Server Error', 'Error: Please, Entry port number between 4000 and 6000!')
        except ValueError:
            messagebox.showerror('Server Error', 'Error: Please, Entry just number!')

    def join_game(self):
        self.port_var = StringVar()
        self.port_Label = Label(self.window, relief=GROOVE, text='Entry Port', bg='lemon chiffon')
        self.port_Label.place(x=50, y=100, width=100, height=20)
        self.port_entry = Entry(self.window, textvariable=self.port_var, font=('calibre', 10, 'normal'))
        self.port_entry.place(x=150, y=100, width=70, height=20)

        self.ip = StringVar()
        self.ip_label = Label(self.window, relief=GROOVE, text='Entry Port', bg='lemon chiffon')
        self.ip_label.place(x=50, y=150, width=100, height=20)
        self.ip_entry = Entry(self.window, textvariable=self.port_var, font=('calibre', 10, 'normal'))
        self.ip_entry.place(x=150, y=150, width=70, height=20)

        self.start_Button = Button(self.window, text='Join Game', command=self.join, bg='orange')
        self.start_Button.place(x=200, y=200, width=80, height=30)
        self.back_button = Button(self.window, relief=RAISED, text='<--', bg='salmon',
                                  font=('Mongolian Baiti', 15, 'normal'))

        self.back_button.configure(command=self.starting)
        self.back_button.place(x=20, y=520, height=20, width=40)

    def join(self):
        a = str(self.port_var.get())
        try:
            if int(a) in range(4000, 6000):
                self.start_Button.destroy()
                self.port_Label.destroy()
                self.port_entry.destroy()
                self.port = int(a)
                p = str(self.ip.get())
                self.server = p
                new_window_2 = Toplevel(self.window)
                start_new_thread(TicToc_Multiplayer, (new_window_2, self.port, str(self.server)))

            else:
                messagebox.showerror('Server Error', 'Error: Please, Entry port number between 4000 and 6000!')
        except ValueError:
            messagebox.showerror('Server Error', 'Error: Please, Entry just number!')

    def multiplayer(self):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()

        self.create_game_button = Button(self.window, relief=RAISED, text='Create Game', bg='salmon',
                                         font=('Mongolian Baiti', 15, 'normal'), command=self.create_game)
        self.join_game_button = Button(self.window, relief=RAISED, text='Join Game', bg='salmon',
                                       font=('Mongolian Baiti', 15, 'normal'), command=self.join_game)
        self.back_button = Button(self.window, relief=RAISED, text='<--', bg='salmon',
                                  font=('Mongolian Baiti', 15, 'normal'))
        self.create_game_button.place(x=120, y=250, height=25, width=200)
        self.join_game_button.place(x=120, y=280, height=25, width=200)
        self.back_button.configure(command=self.starting)
        self.back_button.place(x=20, y=520, height=20, width=40)

    def solo(self):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()
        new_window = Toplevel(self.window)
        start_new_thread(TicToc_Solo, (new_window, ))

        self.back_button = Button(self.window, relief=RAISED, text='<--', bg='salmon',
                                  font=('Mongolian Baiti', 15, 'normal'))
        self.back_button.configure(command=self.starting)
        self.back_button.place(x=20, y=520, height=20, width=40)

    def vs_computer(self):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()
        new_window = Toplevel(self.window)
        start_new_thread(TicToc_Computer, (new_window, ))

        self.back_button = Button(self.window, relief=RAISED, text='<--', bg='salmon',
                                  font=('Mongolian Baiti', 15, 'normal'))
        self.back_button.configure(command=self.starting)
        self.back_button.place(x=20, y=520, height=20, width=40)

    def guide(self):
        pass


