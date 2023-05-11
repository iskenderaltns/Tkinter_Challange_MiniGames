from tkinter import *
from tkinter import messagebox
import socket
import pickle
from _thread import *


class TicToc_Multiplayer(Frame):
    def __init__(self, main_screen, x, y):
        Frame.__init__(self, main_screen, padx=30, pady=30)
        # setting windows
        self.window = main_screen
        self.width = 600
        self.height = 600
        self.window.wm_iconbitmap('servericon.ico')
        self.window.title("TicToc")
        self.window.minsize(width=300, height=300)
        self.window.maxsize(width=300, height=300)
        self.window.geometry("300x300+50+50")
        self.window.configure(bg='cyan3')
        self.pack()

        # server network
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = x
        self.addr = (self.server, self.port)
        self.p = self.connect()
        self.game = None

        # player, list of moves etc.
        self.player = None  # 0 => X ,  1 => O
        self.played_list = []
        self.client_list = []


        # bord of xox , 9 buttons
        self.Button_1 = None
        self.Button_2 = None
        self.Button_3 = None
        self.Button_4 = None
        self.Button_5 = None
        self.Button_6 = None
        self.Button_7 = None
        self.Button_8 = None
        self.Button_9 = None


        # counter of victories
        self.x_var = 0
        self.o_var = 0
        self.label_x = None
        self.label_o = None

        # starting, Choose Teams , X or O, etc./
        self.start_bool = True
        self.turn_bool = False
        self.label_text = Label(self.window, text='...Choose Teams...', font=('calibre', 10, 'normal'), bg='cyan3')
        self.x_button = Button(self.window, text='X', font=('calibre', 10, 'normal'),
                               command=lambda: self.player_x_o('x'))
        self.o_button = Button(self.window, text='O', font=('calibre', 10, 'normal'),
                               command=lambda: self.player_x_o('o'))
        self.label_text.place(x=90, y=70, width=120, height=20)
        self.x_button.place(x=75, y=125, width=50, height=50)
        self.o_button.place(x=175, y=125, width=50, height=50)

        # restart button, you won, lost  label
        self.restart_button = None
        self.won_lost_label = None
        self.restart_bool = False
        self.label_wait = None
        # on commence
        start_new_thread(self.starting, ())


    def starting(self):
        while True:
            try:
                self.game = self.send_data('get')
            except socket.error:
                messagebox.showerror('Attribute Error', "opponent is not tied to the game!")
            if self.start_bool is not False:
                if self.player is not None:

                    if self.game.ready is not False:
                        self.x_button.destroy()
                        self.o_button.destroy()
                        self.label_text.destroy()
                        self.show_buttons()
                        self.start_bool = False

                    else:
                        self.x_button.configure(state=DISABLED)
                        self.o_button.configure(state=DISABLED)
                        self.label_text.configure(text='Waiting for player')
                else:
                    if int(self.p) == 1 and self.game.player0 is not None:
                        if self.game.player0 == 'x':
                            self.x_button.configure(state=DISABLED, bg='red')
                        else:
                            self.o_button.configure(state=DISABLED, bg='red')
                    if int(self.p) == 0 and self.game.player1 is not None:
                        if self.game.player1 == 'x':
                            self.x_button.configure(state=DISABLED, bg='red')
                        else:
                            self.o_button.configure(state=DISABLED, bg='red')

            else:

                if self.restart_bool:
                    self.reset()
                else:
                    self.take_data()
                    self.button_active_normal()

    def player_x_o(self, n):
        # kullanici x  mi o oldugunu secti ve secimi ve id sini servere yolladi 0 numarali kullaci x i secti vs
        if n == 'x':
            self.player = 'x'
            self.game = self.send_data("s:x:"+str(self.p))
        else:
            self.player = 'o'
            self.game = self.send_data("s:o:"+str(self.p))

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except ConnectionRefusedError:
            messagebox.showerror('Connection Error', "Couldn't find a server to connect to !")

    def send_data(self, data):
        try:
            self.client.send(str.encode(data))
            received_data = self.client.recv(2048)
            if received_data:
                return pickle.loads(received_data)
            else:
                raise Exception("No data received from server.")
        except socket.error:
            messagebox.showerror('Attribute Error', "opponent is not tied to the game!")

    def button_active(self, x):
        list_button = [self.Button_1, self.Button_2, self.Button_3, self.Button_4, self.Button_5, self.Button_6,
                       self.Button_7, self.Button_8, self.Button_9]
        if str(list_button[x - 1].cget('text')).lower() not in ['x', 'o']:
            self.game = self.send_data("p" + str(":") + str(self.p) + str(":") + str(x))
            if self.player == 'x':
                list_button[x - 1].configure(text="X", state=DISABLED, command=None)
            else:
                list_button[x - 1].configure(text="O", state=DISABLED, command=None)

            self.played_list.append(x)
            self.play_game(self.played_list)

    def show_buttons(self):
        self.Button_1 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(1))
        self.Button_2 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(2))
        self.Button_3 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(3))
        self.Button_4 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(4))
        self.Button_5 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(5))
        self.Button_6 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(6))
        self.Button_7 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(7))
        self.Button_8 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(8))
        self.Button_9 = Button(self.window, text=None, bg='burlywood3', fg="yellow",
                               command=lambda: self.button_active(9))
        self.Button_1.place(x=50, y=50, height=50, width=50)
        self.Button_2.place(x=110, y=50, height=50, width=50)
        self.Button_3.place(x=170, y=50, height=50, width=50)
        self.Button_4.place(x=50, y=110, height=50, width=50)
        self.Button_5.place(x=110, y=110, height=50, width=50)
        self.Button_6.place(x=170, y=110, height=50, width=50)
        self.Button_7.place(x=50, y=170, height=50, width=50)
        self.Button_8.place(x=110, y=170, height=50, width=50)
        self.Button_9.place(x=170, y=170, height=50, width=50)
        self.label_x = Label(self.window, text='X: ' + str(self.x_var), font=('calibre', 10, 'normal'), bg='VioletRed1')
        self.label_o = Label(self.window, text='O: ' + str(self.o_var), font=('calibre', 10, 'normal'), bg='orchid1')
        self.label_x.place(x=250, y=100, height=30, width=30)
        self.label_o.place(x=250, y=150, height=30, width=30)

    def play_game(self, p):
        if self.in_list([1, 5, 9], p):
            self.Button_1.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(p)
        elif self.in_list([1, 2, 3], p):
            self.Button_1.configure(bg='red')
            self.Button_2.configure(bg='red')
            self.Button_3.configure(bg='red')
            self.finish(p)
        elif self.in_list([4, 5, 6], p):
            self.Button_4.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_6.configure(bg='red')
            self.finish(p)
        elif self.in_list([7, 8, 9], p):
            self.Button_7.configure(bg='red')
            self.Button_8.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(p)
        elif self.in_list([3, 5, 7], p):
            self.Button_3.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_7.configure(bg='red')
            self.finish(p)
        elif self.in_list([1, 4, 7], p):
            self.Button_1.configure(bg='red')
            self.Button_4.configure(bg='red')
            self.Button_7.configure(bg='red')
            self.finish(p)
        elif self.in_list([2, 5, 8], p):
            self.Button_2.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_8.configure(bg='red')
            self.finish(p)
        elif self.in_list([3, 6, 9], p):
            self.Button_3.configure(bg='red')
            self.Button_6.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(p)
        else:
            if len(p) == 5:
                self.game = self.send_data('tie')
                self.tie_control()

    @staticmethod
    def in_list(m, t):
        for i in m:
            if i not in t:
                return False
            else:
                continue
        return True

    def take_data(self):
        if self.game.bool_reset[int(self.p)] is not None:
            self.game = self.send_data('y:' + str(self.p))
        list_button = [self.Button_1, self.Button_2, self.Button_3, self.Button_4, self.Button_5, self.Button_6,
                       self.Button_7, self.Button_8, self.Button_9]
        if self.game.get_move(int(self.p)) is not None:
            a = int(self.game.get_move(int(self.p)))
            if str(list_button[a - 1].cget('text')).lower() not in ['x', 'o']:
                if a not in self.client_list:
                    self.client_list.append(a)

                    if self.player == 'x':

                        list_button[a - 1].configure(text='0', state=DISABLED, command=None)

                    else:
                        list_button[a - 1].configure(text='X', state=DISABLED, command=None)

                    self.play_game(self.client_list)

    def button_active_normal(self):
        list_button = [self.Button_1, self.Button_2, self.Button_3, self.Button_4, self.Button_5, self.Button_6,
                       self.Button_7, self.Button_8, self.Button_9]
        if int(self.p) != int(self.game.turn):
            for b in list_button:
                b.configure(state=DISABLED)

        else:
            for b in list_button:
                if str(b.cget('text')).lower() != 'x' or str(b.cget('text')).lower() != 'o':
                    b.configure(state=NORMAL)
                else:
                    b.configure(state=DISABLED)

    def finish(self, p):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.configure(state=DISABLED, bg='gray64')
        self.restart_button = Button(self.window, text='restart', font=('comicsan', 10, 'bold'), command=self.restart, bg='medium spring green')
        self.restart_button.place(x=110, y=130, height=40, width=80)
        if p == self.played_list:
            if self.player == 'x':
                self.won_lost_label = Label(self.window, text='X Won', font=('comicsan', 10, 'bold'),
                                            bg='light slate gray')
                self.won_lost_label.place(x=100, y=80, width=100, height=20)
                self.x_var += 1
            else:
                self.won_lost_label = Label(self.window, text='O Won', font=('comicsan', 10, 'bold'),
                                            bg='light slate gray')
                self.won_lost_label.place(x=100, y=80, width=100, height=20)
                self.o_var += 1

        else:
            if self.player == 'x':
                self.won_lost_label = Label(self.window, text='O Won', font=('comicsan', 10, 'bold'),
                                            bg='light slate gray')
                self.won_lost_label.place(x=100, y=80, width=100, height=20)
                self.o_var += 1
            else:
                self.won_lost_label = Label(self.window, text='X Won', font=('comicsan', 10, 'bold'),
                                            bg='light slate gray')
                self.won_lost_label.place(x=100, y=80, width=100, height=20)
                self.x_var += 1

    def reset(self):
        if self.game.bool_reset[0] and self.game.bool_reset[1]:
            self.played_list = []
            self.client_list = []
            self.won_lost_label.destroy()
            self.restart_button.destroy()
            if self.label_wait is not None:
                self.label_wait.destroy()
            self.show_buttons()
            self.restart_bool = False

        else:
            if int(self.p) == 0 and self.game.bool_reset[1] is not True and self.game.bool_reset[0] is True:
                for b in Frame.winfo_children(self.window):
                    if str(type(b)) == "<class 'tkinter.Button'>":
                        b.destroy()
                self.won_lost_label.destroy()
                self.label_wait = Label(self.window, text='Waiting for player', font=('calibre', 10, 'normal'),
                                   bg='cyan3')
                self.label_wait.place(x=100, y=80, width=100, height=20)

            if int(self.p) == 1 and self.game.bool_reset[0] is not True and self.game.bool_reset[1] is True:
                for b in Frame.winfo_children(self.window):
                    if str(type(b)) == "<class 'tkinter.Button'>":
                        b.destroy()
                self.won_lost_label.destroy()
                self.label_wait = Label(self.window, text='Waiting for player', font=('calibre', 10, 'normal'),
                                   bg='cyan3')
                self.label_wait.place(x=100, y=80, width=100, height=20)

    def tie_control(self):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.configure(state=DISABLED, bg='gray64')
        self.restart_button = Button(self.window, text='restart', font=('comicsan', 10, 'bold'),
                                     command=self.restart,
                                     bg='medium spring green')
        self.restart_button.place(x=110, y=130, height=40, width=80)
        self.won_lost_label = Label(self.window, text='...tie..', font=('comicsan', 10, 'bold'),
                                    bg='light slate gray')
        self.won_lost_label.place(x=100, y=80, width=100, height=20)

    def restart(self):

        self.game = self.send_data("reset:"+str(self.p))
        self.restart_bool = True

