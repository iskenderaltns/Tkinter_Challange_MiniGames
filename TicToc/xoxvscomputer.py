import random
from tkinter import *

class TicToc_Computer(Frame):
    def __init__(self, main_screen):
        Frame.__init__(self, main_screen, padx=30, pady=30)

        self.window = main_screen
        self.width = 600
        self.height = 600
        self.window.wm_iconbitmap('servericon.ico')
        self.window.title("TicToc")
        self.window.minsize(width=300, height=300)
        self.window.maxsize(width=300, height=300)
        self.window.geometry("300x300+50+50")
        self.window.configure(bg='cyan3')

        self.player = None  # 0 = X ,  1 = 0
        self.played_list = []
        self.computer_list = []
        self.turn = 1
        self.x_var = 0
        self.o_var = 0
        self.pack()

        self.Button_1 = None
        self.Button_2 = None
        self.Button_3 = None
        self.Button_4 = None
        self.Button_5 = None
        self.Button_6 = None
        self.Button_7 = None
        self.Button_8 = None
        self.Button_9 = None
        self.label_text = Label(self.window, text='Choose One', font=('calibre', 10, 'normal'), bg='cyan3')
        self.label_x = None
        self.label_o = None
        self.x_button = Button(self.window, text='X', font=('calibre', 10, 'normal'), command=lambda: self.player_x_o(0))
        self.o_button = Button(self.window, text='O', font=('calibre', 10, 'normal'), command=lambda: self.player_x_o(1))
        self.label_text.place(x=90, y=70, width=120, height=20)
        self.x_button.place(x=75, y=125, width=50, height=50)
        self.o_button.place(x=175, y=125, width=50, height=50)
        self.restart_button = None
        self.won_lost_label = None
        self.moves = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.moves_computer = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9]]


    def player_x_o(self, n):
        if n == 0:
            self.player = 0
        else:
            self.player = 1
        self.label_text.destroy()
        self.x_button.destroy()
        self.o_button.destroy()
        self.show_buttons()

    def computer_playing(self, x):
        list_button = [self.Button_1, self.Button_2, self.Button_3, self.Button_4, self.Button_5, self.Button_6,
                       self.Button_7, self.Button_8, self.Button_9]

        if len(self.played_list) == 1:
            if x == 5:
                a = random.choice([1, 3, 7, 9])
                if self.player == 0:
                    list_button[a-1].configure(text='O', state=DISABLED)
                else:
                    list_button[a - 1].configure(text='X', state=DISABLED)
                self.computer_list.append(a)
                for j in self.moves_computer:
                    if a in j:
                        j.remove(a)
                    else:
                        continue

            elif x in [1, 3, 7, 9]:
                self.computer_list.append(5)
                for j in self.moves_computer:
                    if 5 in j:
                        j.remove(5)
                    else:
                        continue
                if self.player == 0:
                    list_button[4].configure(text='O', state=DISABLED)
                else:
                    list_button[4].configure(text='X', state=DISABLED)

            else:
                if x == 2:
                    self.computer_list.append(3)
                    for j in self.moves_computer:
                        if 3 in j:
                            j.remove(3)
                        else:
                            continue
                    if self.player == 0:
                        list_button[2].configure(text='O', state=DISABLED)
                    else:
                        list_button[2].configure(text='X', state=DISABLED)
                if x == 4:
                    self.computer_list.append(7)
                    for j in self.moves_computer:
                        if 7 in j:
                            j.remove(7)
                        else:
                            continue
                    if self.player == 0:
                        list_button[6].configure(text='O', state=DISABLED)
                    else:
                        list_button[6].configure(text='X', state=DISABLED)
                if x == 6 or x == 8:
                    self.computer_list.append(9)
                    for j in self.moves_computer:
                        if 9 in j:
                            j.remove(9)
                        else:
                            continue
                    if self.player == 0:
                        list_button[8].configure(text='O', state=DISABLED)
                    else:
                        list_button[8].configure(text='X', state=DISABLED)

        else:
            if self.control_move()[0] is not False:
                a = self.control_move()[1]
                for j in self.moves_computer:
                    if a in j:
                        j.remove(a)
                    else:
                        continue
                if self.player == 0:
                    list_button[a - 1].configure(text='O', state=DISABLED)
                else:
                    list_button[a - 1].configure(text='X', state=DISABLED)
                self.computer_list.append(a)
            else:
                if self.control_move_2()[0] is not False:
                    a = self.control_move_2()[1]
                    if self.player == 0:
                        list_button[a - 1].configure(text='O', state=DISABLED)
                    else:
                        list_button[a - 1].configure(text='X', state=DISABLED)
                    self.computer_list.append(a)
                    for j in self.moves_computer:
                        if a in j:
                            j.remove(a)
                        else:
                            continue
                else:
                    try :
                        a = self.random_button()
                        if self.player == 0:
                            list_button[a - 1].configure(text='O', state=DISABLED)
                        else:
                            list_button[a - 1].configure(text='X', state=DISABLED)
                        self.computer_list.append(a)
                        for j in self.moves_computer:
                            if a in j:
                                j.remove(a)
                            else:
                                continue
                    except IndexError:
                        self.play_game(self.computer_list)

        self.play_game(self.computer_list)
        self.turn = 1

    def random_button(self):
        k = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in self.played_list:
            k.remove(i)
        for j in self.computer_list:
            k.remove(j)

        a = random.choice(k)
        return a

    def counter_in_moves(self, l, t):
        c = 0
        for i in self.computer_list:
            if i in l:
                c += 1
        if c == t:
            for i in l:
                if i not in self.computer_list:
                    return i
                else:
                    continue
            return False
        return False

    def control_move(self):
        for move in self.moves:
            if len(move) == 3 and self.counter_in_moves(move, 2) is not False:
                a = self.counter_in_moves(move, 2)
                return True, a
            elif len(move) == 1 and move[0] not in self.computer_list:
                return True, move[0]
            else:
                continue
        return False, None

    def control_move_2(self):
        for move in self.moves_computer:
            if len(move) == 2:
                a = random.choice(move)
                return True, a
            else:
                continue
        return False, None

    def button_active(self, x):
        if self.turn == 1:
            list_button = [self.Button_1, self.Button_2, self.Button_3, self.Button_4, self.Button_5, self.Button_6,
                           self.Button_7, self.Button_8, self.Button_9]

            if self.player == 0:

                list_button[x - 1].configure(text='X', state=DISABLED)
                self.played_list.append(x)
                for i in self.moves_computer:
                    if x in i:
                        i.clear()
                    else:
                        continue

                for j in self.moves:
                    if x in j:
                        j.remove(x)
                    else:
                        continue
                self.play_game(self.played_list)

            else:

                list_button[x - 1].configure(text='O', state=DISABLED)
                self.played_list.append(x)
                for i in self.moves_computer:
                    if x in i:
                        i.clear()
                    else:
                        continue

                for j in self.moves:
                    if x in j:
                        j.remove(x)
                    else:
                        continue

                self.play_game(self.played_list)
            self.turn = 0
            self.computer_playing(x)

    def show_buttons(self):
        self.label_text.destroy()
        self.Button_1 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(1))
        self.Button_2 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(2))
        self.Button_3 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(3))
        self.Button_4 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(4))
        self.Button_5 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(5))
        self.Button_6 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(6))
        self.Button_7 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(7))
        self.Button_8 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(8))
        self.Button_9 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(9))
        self.Button_1.place(x=50, y=50, height=50, width=50)
        self.Button_2.place(x=110, y=50, height=50, width=50)
        self.Button_3.place(x=170, y=50, height=50, width=50)
        self.Button_4.place(x=50, y=110, height=50, width=50)
        self.Button_5.place(x=110, y=110, height=50, width=50)
        self.Button_6.place(x=170, y=110, height=50, width=50)
        self.Button_7.place(x=50, y=170, height=50, width=50)
        self.Button_8.place(x=110, y=170, height=50, width=50)
        self.Button_9.place(x=170, y=170, height=50, width=50)
        self.label_x = Label(self.window, text='X: '+str(self.x_var), font=('calibre', 10, 'normal'), bg='VioletRed1')
        self.label_o = Label(self.window, text='O: '+str(self.o_var), font=('calibre', 10, 'normal'), bg='orchid1')
        self.label_x.place(x=250, y=100, height=30, width=30)
        self.label_o.place(x=250, y=150, height=30, width=30)

    def play_game(self, l):

        if self.in_list([1, 5, 9], l):
            self.Button_1.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(l)
        if self.in_list([1, 2, 3], l):
            self.Button_1.configure(bg='red')
            self.Button_2.configure(bg='red')
            self.Button_3.configure(bg='red')
            self.finish(l)
        if self.in_list([4, 5, 6], l):
            self.Button_4.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_6.configure(bg='red')
            self.finish(l)
        if self.in_list([7, 8, 9], l):
            self.Button_7.configure(bg='red')
            self.Button_8.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(l)
        if self.in_list([3, 5, 7], l):
            self.Button_3.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_7.configure(bg='red')
            self.finish(l)
        if self.in_list([1, 4, 7], l):
            self.Button_1.configure(bg='red')
            self.Button_4.configure(bg='red')
            self.Button_7.configure(bg='red')
            self.finish(l)
        if self.in_list([2, 5, 8], l):
            self.Button_2.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_8.configure(bg='red')
            self.finish(l)
        if self.in_list([3, 6, 9], l):
            self.Button_3.configure(bg='red')
            self.Button_6.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(l)
        else:
            if len(l) == 5:
                self.tie()
            else:
                return None

    @staticmethod
    def in_list(m, t):
        for i in m:
            if i not in t:
                return False
            else:
                continue
        return True

    def finish(self, l):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.configure(state=DISABLED, bg='gray64')
        self.restart_button = Button(self.window, text='restart', font=('comicsan', 10, 'bold'), command=self.restart, bg='medium spring green')
        self.restart_button.place(x=110, y=130, height=40, width=80)
        if l == self.computer_list:
            self.won_lost_label = Label(self.window, text='You lost...', font=('comicsan', 10, 'bold'), bg='light slate gray')
            self.won_lost_label.place(x=100, y=80, width=100, height=20)
            if self.player == 0:
                self.o_var += 1
            else:
                self.x_var += 1
        else:
            self.won_lost_label = Label(self.window, text='You Won...', font=('comicsan', 10, 'bold'), bg='light slate gray')
            self.won_lost_label.place(x=100, y=80, width=100, height=20)
            if self.player == 0:
                self.o_var += 1
            else:
                self.x_var += 1

    def restart(self):
        self.moves = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.moves_computer = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.played_list = []
        self.computer_list = []
        self.turn = 1
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()
        self.won_lost_label.destroy()
        self.show_buttons()

    def tie(self):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.configure(state=DISABLED, bg='gray64')
        self.won_lost_label = Label(self.window, text='Tie...', font=('comicsan', 10, 'bold'),
                                    bg='light slate gray')
        self.won_lost_label.place(x=100, y=80, width=100, height=20)
        self.restart_button = Button(self.window, text='restart', font=('comicsan', 10, 'bold'), command=self.restart, bg='medium spring green')
        self.restart_button.place(x=110, y=130, height=40, width=80)


class TicToc_Solo(Frame):
    def __init__(self, main_screen):
        Frame.__init__(self, main_screen, padx=30, pady=30)

        self.window = main_screen
        self.width = 600
        self.height = 600
        self.window.wm_iconbitmap('servericon.ico')
        self.window.title("TicToc")
        self.window.minsize(width=300, height=300)
        self.window.maxsize(width=300, height=300)
        self.window.geometry("300x300+50+50")
        self.window.configure(bg='cyan3')

        self.player = None
        self.player_2 = None  # 0 = X ,  1 = 0
        self.played_list = []
        self.played_2_list = []
        self.turn = 0
        self.x_var = 0
        self.o_var = 0
        self.pack()

        self.Button_1 = None
        self.Button_2 = None
        self.Button_3 = None
        self.Button_4 = None
        self.Button_5 = None
        self.Button_6 = None
        self.Button_7 = None
        self.Button_8 = None
        self.Button_9 = None
        self.label_text = Label(self.window, text='For Player 1... ', font=('calibre', 10, 'normal'), bg='cyan3')
        self.label_x = None
        self.label_o = None
        self.x_button = Button(self.window, text='X', font=('calibre', 10, 'normal'),
                               command=lambda: self.player_x_o(0))
        self.o_button = Button(self.window, text='O', font=('calibre', 10, 'normal'),
                               command=lambda: self.player_x_o(1))
        self.label_text.place(x=90, y=70, width=120, height=20)
        self.x_button.place(x=75, y=125, width=50, height=50)
        self.o_button.place(x=175, y=125, width=50, height=50)
        self.restart_button = None
        self.won_lost_label = None



    def player_x_o(self, n):
        if n == 0:
            self.player = 0
        else:
            self.player = 1
        self.label_text.destroy()
        self.x_button.destroy()
        self.o_button.destroy()
        self.show_buttons()

    def button_active(self, x):
        list_button = [self.Button_1, self.Button_2, self.Button_3, self.Button_4, self.Button_5, self.Button_6,
                       self.Button_7, self.Button_8, self.Button_9]
        if self.turn == 0:
            list_button[x - 1].configure(text='X', state=DISABLED)
            self.played_list.append(x)
            self.play_game(self.played_list)
            self.turn = 1
        else:
            list_button[x - 1].configure(text='O', state=DISABLED)
            self.played_2_list.append(x)
            self.play_game(self.played_2_list)
            self.turn = 0

    def show_buttons(self):
        self.Button_1 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(1))
        self.Button_2 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(2))
        self.Button_3 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(3))
        self.Button_4 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(4))
        self.Button_5 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(5))
        self.Button_6 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(6))
        self.Button_7 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(7))
        self.Button_8 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(8))
        self.Button_9 = Button(self.window, text=None, bg='burlywood3', fg="yellow", command=lambda: self.button_active(9))
        self.Button_1.place(x=50, y=50, height=50, width=50)
        self.Button_2.place(x=110, y=50, height=50, width=50)
        self.Button_3.place(x=170, y=50, height=50, width=50)
        self.Button_4.place(x=50, y=110, height=50, width=50)
        self.Button_5.place(x=110, y=110, height=50, width=50)
        self.Button_6.place(x=170, y=110, height=50, width=50)
        self.Button_7.place(x=50, y=170, height=50, width=50)
        self.Button_8.place(x=110, y=170, height=50, width=50)
        self.Button_9.place(x=170, y=170, height=50, width=50)
        self.label_x = Label(self.window, text='X: '+str(self.x_var), font=('calibre', 10, 'normal'), bg='VioletRed1')
        self.label_o = Label(self.window, text='O: '+str(self.o_var), font=('calibre', 10, 'normal'), bg='orchid1')
        self.label_x.place(x=250, y=100, height=30, width=30)
        self.label_o.place(x=250, y=150, height=30, width=30)

    def play_game(self, l):

        if self.in_list([1, 5, 9], l):
            self.Button_1.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(l)
        if self.in_list([1, 2, 3], l):
            self.Button_1.configure(bg='red')
            self.Button_2.configure(bg='red')
            self.Button_3.configure(bg='red')
            self.finish(l)
        if self.in_list([4, 5, 6], l):
            self.Button_4.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_6.configure(bg='red')
            self.finish(l)
        if self.in_list([7, 8, 9], l):
            self.Button_7.configure(bg='red')
            self.Button_8.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(l)
        if self.in_list([3, 5, 7], l):
            self.Button_3.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_7.configure(bg='red')
            self.finish(l)
        if self.in_list([1, 4, 7], l):
            self.Button_1.configure(bg='red')
            self.Button_4.configure(bg='red')
            self.Button_7.configure(bg='red')
            self.finish(l)
        if self.in_list([2, 5, 8], l):
            self.Button_2.configure(bg='red')
            self.Button_5.configure(bg='red')
            self.Button_8.configure(bg='red')
            self.finish(l)
        if self.in_list([3, 6, 9], l):
            self.Button_3.configure(bg='red')
            self.Button_6.configure(bg='red')
            self.Button_9.configure(bg='red')
            self.finish(l)
        else:
            if len(l) == 5:
                self.tie()
            else:
                return None
    @staticmethod
    def in_list(m, t):
        for i in m:
            if i not in t:
                return False
            else:
                continue
        return True

    def finish(self, l):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.configure(state=DISABLED, bg='gray64')
        self.restart_button = Button(self.window, text='restart', font=('comicsan', 10, 'bold'), command=self.restart, bg='medium spring green')
        self.restart_button.place(x=110, y=130, height=40, width=80)
        if l == self.played_list:
            self.won_lost_label = Label(self.window, text='X Won', font=('comicsan', 10, 'bold'), bg='light slate gray')
            self.won_lost_label.place(x=100, y=80, width=100, height=20)
            self.x_var += 1
        else:
            self.won_lost_label = Label(self.window, text='O Won', font=('comicsan', 10, 'bold'), bg='light slate gray')
            self.won_lost_label.place(x=100, y=80, width=100, height=20)
            self.o_var += 1

    def restart(self):
        self.played_list = []
        self.played_2_list = []
        self.turn = 0
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.destroy()
        self.won_lost_label.destroy()
        self.show_buttons()

    def tie(self):
        for b in Frame.winfo_children(self.window):
            if str(type(b)) == "<class 'tkinter.Button'>":
                b.configure(state=DISABLED, bg='gray64')
        self.restart_button = Button(self.window, text='restart', font=('comicsan', 10, 'bold'), command=self.restart, bg='medium spring green')
        self.restart_button.place(x=110, y=130, height=40, width=80)

