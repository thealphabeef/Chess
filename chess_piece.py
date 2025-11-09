from abc import ABC, abstractmethod
from move import Move
from player import Player

class ChessPiece(ABC):
    """Abstract base class for all chess pieces.

    Attributes:
        player (Player): Owner of the piece.
    """
    def __init__(self, player: Player):
        """Initialize a chess piece.

        Args:
            player (Player): Owner of the piece.
        """
        self.__player = player

    @property
    def player(self) -> Player:
        """Player: The owner of the piece."""
        return self.__player

    @abstractmethod
    def __str__(self) -> str:
        """Return the readable name for the piece."""

    @abstractmethod
    def type(self) -> str:
        """Return the display type for the piece."""

    def is_valid_move(self, move: Move, board: list[list['ChessPiece']]) -> bool:
        """Check structural movement rules shared by all pieces.

        Args:
            move (Move): The proposed move.
            board (list[list['ChessPiece']]): The board to validate against.

        Returns:
            bool: ''True'' if the move satisfies the base constraints, ''False'' otherwise.
        """
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
