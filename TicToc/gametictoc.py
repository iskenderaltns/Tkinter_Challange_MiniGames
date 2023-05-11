class Game:
    def __init__(self, id):
        self.player0 = None
        self.player1 = None
        self.id = id
        self.move0 = []
        self.move1 = []
        self.ready = False
        self.tie_bool = None
        self.turn = None
        self.bool_reset = [None, None]



    def both_went(self, t, n):  # bu kisim tamam

        if n == 0:
            self.player0 = t
        if n == 1:
            self.player1 = t

        if t == 'x':
            self.turn = n

        if self.player1 is not None and self.player0 is not None:
            self.ready = True

    def reset_repair(self, id):
        self.bool_reset[int(id)] = None

    def reset(self, id):
        self.bool_reset[int(id)] = True
        if self.bool_reset[0] is True and self.bool_reset[1] is True:
            self.move1.clear()
            self.move0.clear()
            if self.player0 == 'x':
                self.turn = 0
            else:
                self.turn = 1

            self.tie_bool = None


    def tie(self):
        self.tie_bool = True

    def which_move(self, p, x): # bu kisim tamam
        if p == 0:
            self.move0.append(int(x))
            self.turn = 1
        if p == 1:
            self.move1.append(int(x))
            self.turn = 0

    def get_move(self, p):
        if p == 0:
            if len(self.move1) != 0:
                return self.move1[-1]
            else:
                return None
        if p == 1:
            if len(self.move0) != 0:
                return self.move0[-1]
            else:
                return None
