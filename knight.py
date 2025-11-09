from chess_piece import ChessPiece
from move import Move

class Knight(ChessPiece):
    """Represents a Knight piece.

    Attributes:
        player (Player): Owner of the Knight.
    """
    def __init__(self, player):
        """Initialize a knight chess piece.

        Args:
            player (Player): Owner of the knight.
        """
        super().__init__(player)

    def __str__(self) -> str:
        """Return the readable name of the knight.

        Returns:
            str: The string ''"Knight"''.
        """
        return 'Knight'

    def type(self) -> str:
        """Return the display type for the knight.

        Returns:
            str: The type name ''"Knight"''.
        """
        return 'Knight'

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        """Determine whether a move is legal for a knight.

        Args:
            move (Move): The candidate move for the knight.
            board (list[list[ChessPiece]]): The current state of the board.

        Returns:
            bool: ''True'' if the knight can legally execute the move, ''False'' otherwise.
        """
        if not super().is_valid_move(move, board):
            return False

        dr = abs(move.to_row - move.from_row)
        dc = abs(move.to_col - move.from_col)
        return (dr, dc) in {(2, 1), (1, 2)}