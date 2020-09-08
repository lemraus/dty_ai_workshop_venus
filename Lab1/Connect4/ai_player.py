from player import Player
from copy import deepcopy


class AIPlayer(Player):
    def __init__(self):
        self.name = "Lemraus"
        self.max_depth = 3
        self.streak_weights = [0, 1, 15, 100, 2000]

    def getColumn(self, board):
        alpha = -1e6
        best_col = None

        for col in board.getPossibleColumns():
            next_board = deepcopy(board)
            row = next_board.play(self.color, col)
            if self.get_play_score(row, col, next_board) > 1000:
                return col
            beta = self.min_step(next_board, 1, 1e6, alpha)
            if beta > alpha:
                alpha = beta
                best_col = col

        return best_col

    def max_step(self, board, depth, min_beta, max_alpha):
        alpha = -1e6
        for col in board.getPossibleColumns():
            next_board = deepcopy(board)
            row = next_board.play(self.color, col)
            score = self.get_play_score(row, col, next_board)
            if score > 1000:
                return score
            if depth == self.max_depth:
                beta = score
            else:
                beta = self.min_step(
                    next_board, depth + 1, min_beta, max(alpha, max_alpha)
                )
            if beta > min_beta:
                return beta
            if beta > alpha:
                alpha = beta
        return alpha

    def min_step(self, board, depth, min_beta, max_alpha):
        beta = 1e6
        for col in board.getPossibleColumns():
            next_board = deepcopy(board)
            row = next_board.play(-self.color, col)
            score = self.get_play_score(row, col, next_board)
            if score < -1000:
                return score
            if depth == self.max_depth:
                alpha = score
            else:
                alpha = self.max_step(
                    next_board, depth + 1, min(beta, min_beta), max_alpha
                )

            if alpha < max_alpha:
                return alpha
            if alpha < beta:
                beta = alpha
        return beta

    def get_play_score(self, row, col, board):
        weights = [
            [5, 8, 11, 13, 11, 8, 5],
            [5, 8, 11, 13, 11, 8, 5],
            [4, 6, 8, 10, 8, 6, 4],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        row_score = self.get_row_score(row, col, board)
        col_score = self.get_col_score(row, col, board)
        diag_score = self.get_diag_score(row, col, board)
        score = weights[row][col] + row_score + col_score + diag_score
        return score

    def get_streaks_score(self, l):
        streak = 0
        score = 0
        prev_val = 0
        for val in l:
            if val == 0:
                prev_val = 0
                streak = 0
                continue
            if val != prev_val:
                streak = 0
            streak += 1
            score += self.color * val * self.streak_weights[min(4, streak)]
            prev_val = val
        return score

    def get_row_score(self, row, col, board):
        row_slice = board.getRow(row)[max(0, col - 3) : min(6, col + 4)]
        return self.get_streaks_score(row_slice)

    def get_col_score(self, row, col, board):
        col_slice = board.getCol(col)[max(0, row - 3) : min(5, row + 4)]
        return self.get_streaks_score(col_slice)

    def get_diag_score(self, row, col, board):
        diag_up_score = self.get_diag_up_score(row, col, board)
        diag_down_score = self.get_diag_down_score(row, col, board)
        return diag_up_score + diag_down_score

    def get_diag_up_score(self, row, col, board):
        diag_up = board.getDiagonal(True, col - row)
        return self.get_streaks_score(diag_up)

    def get_diag_down_score(self, row, col, board):
        diag_down = board.getDiagonal(False, col + row)
        return self.get_streaks_score(diag_down)

