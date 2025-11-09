from chess_piece import ChessPiece
from move import Move

class Queen(ChessPiece):
    def __init__(self, player):
        """Initialize a queen chess piece.

        Args:
            player (Player): Owner of the queen.
        """
        super().__init__(player)

    def __str__(self) -> str:
        """Returns the readable name of the queen.

        Returns:
            str: The string ''"Queen"''.
        """
        return 'Queen'

    def type(self) -> str:
        """Returns the display type for the queen.

        Returns:
            str: The type name ''"Queen"''.
        """
        return 'Queen'

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        """Determine whether a move is legal for a queen.

        Args:
            move (Move): The candidate move for the queen.
            board (list[list[ChessPiece]]): The current board state.

        Returns:
            bool: ''True'' if the queen can legally execute the move, ''False'' otherwise.
        """
        if not super().is_valid_move(move, board):
            return False

        dr = move.to_row - move.from_row
        dc = move.to_col - move.from_col

        #if our logic for bishop and rook are not passing then its false
        if (abs(dr) != abs(dc)) and (dr != 0 and dc != 0):
            return False

        # determine our direction of travel
        row_step = 0 if dr == 0 else (1 if dr > 0 else -1)
        col_step = 0 if dc == 0 else (1 if dc > 0 else -1)

        # check all the squares to the path are empty :)
        r, c = (move.from_row + row_step), (move.from_col + col_step)
        while (r != move.to_row) or (c != move.to_col):
            if board[r][c] is not None:
                return False
            r += row_step
            c += col_step

        # our destination is either empty or enemy
        return True
