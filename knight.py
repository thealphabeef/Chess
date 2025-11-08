from chess_piece import ChessPiece
from move import Move

class Knight(ChessPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self) -> str:
        return 'Knight'

    def type(self) -> str:
        return 'Knight'

    def is_valid_move(self, move: Move, board: list[list['ChessPiece']]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        dr = abs(move.to_row - move.from_row)
        dc = abs(move.to_col - move.from_col)
        return (dr, dc) in {(2, 1), (1, 2)}