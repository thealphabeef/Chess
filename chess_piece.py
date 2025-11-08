from abc import ABC, abstractmethod
from move import Move
from player import Player

class ChessPiece(ABC):
    def __init__(self, player: Player):
        self.__player = player

    @property
    def player(self) -> Player:
        return self.__player

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def type(self) -> str:
        pass

    def is_valid_move(self, move: Move, board: list[list['ChessPiece']]) -> bool:
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        fr, fc, tr, tc = move.from_row, move.from_col, move.to_row, move.to_col

        # 1) indices in-bounds
        if not (0 <= fr < rows and 0 <= fc < cols and 0 <= tr < rows and 0 <= tc < cols):
            return False

        # 2) start and end squares differ
        if fr == tr and fc == tc:
            return False

        # 3) self is on the starting square
        if board[fr][fc] is not self:
            return False

        # 4) destination is not occupied by a same-color piece
        dest_piece = board[tr][tc]
        if dest_piece is not None and dest_piece.player == self.player:
            return False
        return True
