from chess_piece import ChessPiece
from move import Move

class King(ChessPiece):
    def __init__(self, player):
        """Initialize a king chess piece.

        Args:
            player (Player): Owner of the king.
        """
        super().__init__(player)

    def __str__(self) -> str:
        """Returns the readable name of the king.

        Returns:
            str: The string ''"King"''.
        """
        return 'King'

    def type(self) -> str:
        """Returns the display type of the king.

        Returns:
            str: The type name ''"King"''.
        """
        return 'King'

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        """Determine whether a move is legal for a king.

        Args:
            move (Move): The candidate move for the king.
            board (list[list[ChessPiece]]): The current board state.

        Returns:
            bool: ''True'' if the King can legally execute the move, ''False'' otherwise.
        """
        if not super().is_valid_move(move, board):
            return False

        dr = abs(move.to_row - move.from_row)
        dc = abs(move.to_col - move.from_col)
        return max(dr, dc) == 1