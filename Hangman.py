import random
from tkinter import *
from tkinter import messagebox

class Hangman(Frame):
    def __init__(self, main_screen):
        Frame.__init__(self, main_screen, padx=30, pady=30)


        self.window = main_screen
        self.width = 900
        self.height = 600
        self.window.wm_iconbitmap('hmicon.ico')
        self.window.title("Hangman")
        self.window.minsize(width=900, height=600)
        self.window.maxsize(width=900, height=600)
        self.window.geometry("900x600+50+50")
        self.window.configure(bg='cyan3')
        self.pack()

        self.bg_img = PhotoImage(file="hangmannbg.png")
        self.bg_img_Label = Label(self.window, image=self.bg_img)
        self.bg_img_Label.place(x=0, y=0)

        with open('EnglishWords.txt') as f:
            self.words_english = f.read().split()

        self.data_letter = []
        self.score = 0
        self.health = 0
        self.count = 0
        self.control_letter = StringVar()
        self.control_letter_label = Entry(self.window, relief=FLAT, textvariable=self.control_letter)
        self.control_letter_label.place(x=350, y=300, width=40, height=40)

        self.control_letter_button = Button(self.window, relief=GROOVE, text='Control', command=self.control, bg='yellow')
        self.control_letter_button.place(x=400, y=300, width=60, height=40)

        self.control_word = StringVar(value='Please, Entry Word')
        self.control_word_label = Entry(self.window, relief=FLAT, textvariable=self.control_word)
        self.control_word_label.place(x=350, y=450, width=200, height=40)

        self.control_word_button = Button(self.window, relief=GROOVE, text='Control Word', command=self.cont_word, bg='green yellow')
        self.control_word_button.place(x=400, y=500, width=100, height=40)

        self.canvas = Canvas(self.window, width=200, height=400, bg='OrangeRed3')
        self.canvas.place(x=50, y=100)


        self.coordinate = [[30, 30, 30, 370], [30, 30, 130, 30], [30, 80, 80, 30], [130, 30, 130, 80], [110, 80, 150, 120], [130, 120, 130, 200], [130, 120, 90, 170], [130, 120, 170, 170], [130, 200, 90, 260], [130, 200, 170, 260]]
        self.word = random.choice(self.words_english)
        self.words_english.remove(self.word)
        self.labels_letter = []
        self.score_label_2 = None
        self.score_label_ = Label(self.window, relief=FLAT, bg="grey24", text='Your Score:', font=('calibre', 10, 'normal'), fg='OrangeRed3')
        self.score_label_.place(x=700, y=70, width=100, height=50)
        self.score_label = Label(self.window, relief=GROOVE, bg='grey24', text=self.score, fg='white')

        self.finish_label = Label(self.window, relief=GROOVE, bg='OliveDrab1')

        self.game_over_label = Label(self.finish_label, relief=GROOVE, text='Game Over', bg='red',
                                     font=('calibre', 20, 'bold'))
        self.restart_button = Button(self.finish_label, relief=GROOVE, text='Restart', bg='grey', command=self.restart)

        self.show_word = None
        self.starting()

    def cont_word(self):
        word = self.control_word.get().lower()
        if word == self.word.lower():
            for i in range(len(self.word)):
                self.labels_letter[i].configure(text=self.word[i])
                self.win()


    def control(self):
        letter = self.control_letter.get().lower()
        if letter in 'azertyuiopqsdfghjklwxcvbnm' and len(letter) == 1:
            if letter in self.word.lower() and letter not in self.data_letter:
                self.data_letter.append(letter)
                k = [i for i in range(len(self.word)) if self.word[i].lower() == letter]
                for j in k:
                    self.count += 2
                    self.score += 2
                    self.score_label.configure(text=self.score)
                    self.labels_letter[j].configure(text=letter.capitalize())
                    if len(self.word)*2 == self.count:
                        self.win()
            elif letter in self.data_letter:
                messagebox.showerror('Error', 'You used this letter before')
            else:
                self.data_letter.append(letter)
                self.health += 1
                self.punishment()
                if self.health == 10:
                    self.game_over()

        else:
            messagebox.showerror('Error', 'Please enter a valid character')

    def punishment(self):
        if self.health > 0:
            if self.health < 5 or self.health > 5:
                x0, y0, x1, y1 = self.coordinate[self.health-1][0], self.coordinate[self.health-1][1], self.coordinate[self.health-1][2], self.coordinate[self.health-1][3]
                self.canvas.create_line(x0, y0, x1, y1, fill='black', width=4)
            else:
                x0, y0, x1, y1 = self.coordinate[self.health - 1][0], self.coordinate[self.health - 1][1], \
                                 self.coordinate[self.health - 1][2], self.coordinate[self.health - 1][3]
                self.canvas.create_oval(x0, y0, x1, y1, outline='black', width=4)

    def create_labels_letter(self):
        for i in range(len(self.word)):
            label = Label(self.window, relief=FLAT, text=None, bg='gray')
            self.labels_letter.append(label)

    def starting(self):
        self.create_labels_letter()
        for i in range(len(self.word)):
            self.labels_letter[i].place(x=350+(i*50), y=200, height=40, width=40)
            if self.word[i].lower() not in 'azertyuiopqsdfghjklwxcvbnm':
                self.labels_letter[i].configure(text=self.word[i])

        self.score_label.place(x=800, y=70, width=100, height=50)

    def game_over(self):
        self.control_word_button.configure(state=DISABLED)
        self.control_letter_button.configure(state=DISABLED)
        self.finish_label = Label(self.window, relief=GROOVE, bg='OliveDrab1')
        self.finish_label.place(x=300, y=200, width=300, height=200)
        self.show_word = Label(self.finish_label, relief=GROOVE, bg='OliveDrab1', text=str(self.word))
        self.show_word.place(x=100, y=10, width=100, height=30)
        self.game_over_label = Label(self.finish_label, relief=GROOVE, text='Game Over', bg='red',
                                     font=('calibre', 20, 'bold'))
        self.score_label_2 = Label(self.finish_label, relief=GROOVE, bg='OliveDrab1', text='Your Score: '+str(self.score))
        self.restart_button = Button(self.finish_label, relief=GROOVE, text='Restart', bg='gray', command=self.restart)
        self.game_over_label.place(x=50, y=50, width=200, height=50)
        self.score_label_2.place(x=100, y=100, width=100, height=40)
        self.restart_button.place(x=100, y=150, width=100, height=40)


    def win(self):
        a = len(self.word) - (self.count/2)
        b = 10 - self.health
        if a == 0:
            self.score += b*5
        else:
            self.score += (b*5) + a*2
        self.data_letter = []
        self.score_label.configure(text=self.score)
        self.count = 0
        self.health = 0
        self.word = random.choice(self.words_english)
        self.words_english.remove(self.word)
        for i in self.labels_letter:
            i.destroy()
        self.labels_letter = []
        self.canvas.delete('all')
        self.starting()

    def restart(self):
        self.count = 0
        self.health = 0
        self.score = 0
        self.score_label.configure(text=str(self.score))
        self.data_letter = []
        self.word = random.choice(self.words_english)
        self.words_english.remove(self.word)
        for i in self.labels_letter:
            i.destroy()
        self.labels_letter = []
        self.control_word_button.configure(state=NORMAL)
        self.control_letter_button.configure(state=NORMAL)
        self.canvas.delete('all')
        self.restart_button.destroy()
        self.game_over_label.destroy()
        self.finish_label.destroy()
        self.score_label_2.destroy()
        self.starting()

'''
root = Tk()
app = Hangman(root)
app.mainloop()
'''
