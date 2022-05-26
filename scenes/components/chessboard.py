class CBoard:
    
    def __init__(self):
        self.board = {
            "a": [None, ["r", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["r", "b"]],
            "b": [None, ["n", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["n", "b"]],
            "c": [None, ["b", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["b", "b"]],
            "d": [None, ["q", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["q", "b"]],
            "e": [None, ["k", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["k", "b"]],
            "f": [None, ["b", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["b", "b"]],
            "g": [None, ["n", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["n", "b"]],
            "h": [None, ["r", "w"], ["p", "w"], [None, None], [None, None], [None, None], [None, None], ["p", "b"], ["r", "b"]]
        }
        self.turn = True
        self.beaten = {
            "w": [],
            "b": []
        }
    
    def get_board(self):
        return self.board
    
    def pop(self, coords):
        if self.board[coords[0]][int(coords[1])][0]:
            self.beaten[self.board[coords[0]][int(coords[1])][1]].append(self.board[coords[0]][int(coords[1])])
        self.board[coords[0]][int(coords[1])] = [None, None]
    
    def _move(self, x, y):
        self.pop(y)
        self.board[y[0]][int(y[1])] = [self.board[x[0]][int(x[1])][0], self.board[x[0]][int(x[1])][1]]
        self.pop(x)
    
    def push(self, move):
        if move in ("e1h1", "e1g1"):
            if self.board["e"][1][0] == "k":
                self._move("h1", "f1")
                self._move("e1","g1")
        elif move in ("e1a1", "e1c1"):
            if self.board["e"][1][0] == "k":
                self._move("a1", "d1")
                self._move("e1","c1")
        elif move in ("e8h8", "e8g8"):
            if self.board["e"][1][0] == "k":
                self._move("h8", "f8")
                self._move("e8","g8")
        elif move in ("e8a8", "e8c8"):
            if self.board["e"][1][0] == "k":
                self._move("a8", "d8")
                self._move("e8","c8")
        elif self.board[move[0]][int(move[1])][0] == "p" and move[0] != move[2] and not self.board[move[2]][int(move[3])][0]:
            self._move(move[:2], move[2::])
            self.pop((move[2], move[1]))
        else:
            self._move(move[:2], move[2::]) 
        
    def is_promotion(self):
        for lett in self.board:
            if self.board[lett][1][0] == "p" or self.board[lett][8][0] == "p":
                return True
        return False
    
    def promote(self, p):
        for lett in self.board:
            if self.board[lett][1][0] == "p": 
                self.board[lett][1][0] = p
                return
            elif self.board[lett][8][0] == "p":
                self.board[lett][8][0] = p
                return
                         
    def print(self):
        for i in range(1, 9):
            out = ""
            for m in self.board:
                if self.board[m][i][0]:
                    out += self.board[m][i][0]
                else:
                    out += "0"
            print(out)