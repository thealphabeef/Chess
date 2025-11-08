from chess_piece import ChessPiece
from move import Move


class Bishop(ChessPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self) -> str:
        return "Bishop"

    def type(self) -> str:
        return "Bishop"

    def is_valid_move(self, move: Move, board: list[list["ChessPiece"]]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        dr = move.to_row - move.from_row
        dc = move.to_col - move.from_col

        #bishop must move diagonally
        if abs(dr) != abs(dc):
            return False

        #determine our direction of travel
        row_step = 1 if dr > 0 else -1
        col_step = 1 if dc > 0 else -1

        #check all the squares to the path are empty :)
        r, c = (move.from_row + row_step), (move.from_col + col_step)
        while (r != move.to_row) and (c != move.to_col):
            if board[r][c] is not None:
                return False
            r += row_step
            c += col_step

        #our destination is either empty or enemy :(
        return True
