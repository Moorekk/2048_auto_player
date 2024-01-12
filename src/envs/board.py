import random
import itertools
import operator
import numpy as np
def list_transpose(list_2d):
    return list(map(list, zip(*list_2d)))

class _2048board():
    def __init__(self, board_width) -> None:
        self.board_width = board_width
        self.board = np.zeros(())
        self.new_block_range = [1, 2]
        self.init_board()

    def init_board(self):
        self.board = np.zeros((self.board_width, self.board_width), dtype=np.int8)
        # self.board = np.array([[0,0,0,0],
        #                         [1,0,0,0],
        #                         [2,1,3,2],
        #                         [3,4,5,4]])
        # self.board = self.board.T

    def get_board(self):
        return self.board

    def is_full(self):
        return np.all(self.board)

    def is_over(self):
        if not self.is_full(): return False

        # check rows
        for row in self.board:
            if any(map(operator.eq, row, itertools.islice(row, 1, None))):
                return False
        
        # check cols
        for col in list_transpose(self.board):
            if any(map(operator.eq, col, itertools.islice(col, 1, None))):
                return False

        return True
    
    def action_meaning(self, action:int) -> str:
        return {0:'up', 1:'down',2:'left',3:'right'}[action]

    def random_generate(self):
        zero_list = np.stack(np.where(self.board == 0)).T

        # [(i, j) for i in range(len(self.board)) for j in range(len(self.board[0])) if self.board[i][j] == 0]
        new_idx = random.choice(zero_list)
        self.board[new_idx[0], new_idx[1]] = random.choice(self.new_block_range)
        
    def move(self, action):
        # print(action)
        move_score = 0
        board_stuck = True
        match (action):
            case (0):
                for i, line in enumerate(self.board):
                    new_line, line_score = self._move_line(line)
                    if (line != new_line).any(): board_stuck = False
                    self.board[i] = new_line
                    move_score += line_score
            case (1):
                for i, line in enumerate(self.board):
                    new_line, line_score = self._move_line(line[-1::-1])
                    if (line[-1::-1] != new_line).any(): board_stuck = False
                    self.board[i] = new_line[-1::-1]
                    move_score += line_score
            case (2):
                self.board = self.board.T
                for i, line in enumerate(self.board):
                    new_line, line_score = self._move_line(line)
                    if (line != new_line).any(): board_stuck = False
                    self.board[i] = new_line
                    move_score += line_score
                self.board = self.board.T
            case (3):
                self.board = self.board.T
                for i, line in enumerate(self.board):
                    new_line, line_score = self._move_line(line[-1::-1])
                    if (line[-1::-1] != new_line).any(): board_stuck = False
                    self.board[i] = new_line[-1::-1]
                    move_score += line_score
                self.board = self.board.T
        return move_score, board_stuck

    def _move_line(self, line):
        line_score = 0
        stack = []
        merged = False
        for cell in line:
            if cell == 0: continue
            stack.append(cell)

            # merge recursively
            if len(stack) >= 2 and stack[-2] == stack[-1] and not merged:
                merged = True
                stack[-2] += 1
                line_score += 2 ** (stack[-2])
                stack.pop()
            else:
                merged = False
                
        line = stack + [0] * (self.board_width - len(stack))
        return np.array(line, dtype=np.int8), line_score