from tkinter import *
import socket
from tkinter import messagebox
from _thread import *
import pickle
from gametictoc import Game
class Server(Frame):
    def __init__(self, main_screen, x):
        Frame.__init__(self, main_screen, padx=20, pady=20)
        main_screen.wm_iconbitmap('servericon.ico')
        main_screen.title("Server")
        main_screen.minsize(width=300, height=300)
        main_screen.geometry("300x300")
        self.pack()
        self.info = "Waiting for a connection, Server Started"
        self.addr_list = [None, None]
        self.control = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = x


        self.photo_smile = PhotoImage(file='smile.png')
        self.photo_smile_resizing = self.photo_smile.subsample(10, 10)
        self.photo_sad = PhotoImage(file='sad.png')
        self.photo_sad_resizing = self.photo_sad.subsample(10, 10)

        self.player_0 = Button(self, text='  Player 0\nNon Connected\n', relief=GROOVE, width=120, height=120, bg='snow4', image=self.photo_sad_resizing, compound=TOP)
        self.player_1 = Button(self, text='  Player 1\nNon Connected\n', relief=GROOVE, width=120, height=120, bg='snow4', image=self.photo_sad_resizing, compound=TOP)
        self.info_label = Label(self, text='Both Player are connected', relief='flat', width=200, height=30, bg='gray94', font=('consolos', '9'))


        self.selectableMsg = Text(self, width=35, height=2, relief='flat', bg='gray94', wrap='word', font=('consolos', '9'))

        self.connected = set()
        self.games = {}
        self.idCount = 0


        self.kaos()


    def kaos(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)
        try:
            self.s.listen(2)
            start_new_thread(self.start, ())
        except OSError:
            messagebox.showerror('Server Error', 'Error: Please, This port is full. Try another port!')

    def threaded_client(self, conn, p, gameId):

        conn.send(str.encode(str(p)))


        while True:
            try:
                data = conn.recv(4096).decode()

                if gameId in self.games:
                    game = self.games[gameId]

                    if not data:
                        break
                    else:
                        if data != "get" and data[0] != 's' and data != "tie" and data[0] != 'r' and data[0] != 'y':
                            arr = data.split(":")
                            id = int(arr[1])
                            if id == 0:
                                self.player_0.config(bg='yellow')
                                self.player_1.config(bg='green yellow')
                            else:
                                self.player_1.config(bg='yellow')
                                self.player_0.config(bg='green yellow')
                            move = int(arr[2])
                            game.which_move(id, move)
                        elif data[0] == 's':
                            arr = data.split(":")
                            team = str(arr[1])
                            id = int(arr[2])
                            game.both_went(team, id)
                        elif data == "tie":
                            game.tie()

                        elif data[0] == "r":
                            arr = data.split(":")
                            id = arr[1]
                            game.reset(id)
                        elif data[0] == 'y':
                            arr = data.split(":")
                            id = int(arr[1])
                            game.reset_repair(id)
                        conn.sendall(pickle.dumps(game))

            except:
                break

        self.info = 'Lost Connection'
        self.selectableMsg.config(state='normal')
        self.selectableMsg.delete("0.0", "end")
        self.selectableMsg.insert("end", self.info)
        self.selectableMsg.configure(state='disabled')
        try:
            del self.games[gameId]
            if gameId == 0:
                self.player_0.config(text='  Player 0\n Closed game:\n', image=self.photo_sad_resizing, bg='gray94')
                self.player_1.config(bg='gray94')
            else:
                self.player_1.config(text='  Player 1\n Closed game:\n', image=self.photo_sad_resizing, bg='gray94')
                self.player_0.config(bg='gray94')
        except:
            pass
        self.idCount -= 1
        conn.close()

    def start(self):

        while True:

            self.selectableMsg.insert(1.0, self.info)
            self.selectableMsg.configure(state='disabled')
            self.selectableMsg.pack(pady=5)
            self.player_0.pack(side=LEFT)
            self.player_1.pack(side=RIGHT)

            conn, addr = self.s.accept()

            self.idCount += 1
            self.addr_list[self.idCount-1] = str(addr)

            if self.addr_list[0] is not None:
                self.player_0.config(text='  Player 0\n Connected to:\n'+str(self.addr_list[0]), image=self.photo_smile_resizing, bg='green yellow')

            if self.addr_list[1] is not None:
                self.info = 'Both Player are connected'
                self.selectableMsg.config(state='normal')
                self.selectableMsg.delete("0.0", "end")
                self.selectableMsg.insert("end", self.info)
                self.selectableMsg.configure(state='disabled')

                self.player_1.config(text='  Player 1\n Connected to:\n'+str(self.addr_list[1]), image=self.photo_smile_resizing, bg='green yellow')


            p = 0
            gameId = (self.idCount - 1) // 2
            if self.idCount % 2 == 1:
                self.games[gameId] = Game(gameId)
            else:
                p = 1

            start_new_thread(self.threaded_client, (conn, p, gameId))

