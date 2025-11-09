from chess_piece import ChessPiece
from move import Move

class Rook(ChessPiece):
    def __init__(self, player):
        """Initialize a rook chess piece.

        Args:
            player (Player): Owner of the rook.
        """
        super().__init__(player)

    def __str__(self) -> str:
        """Return the readable name of the rook.

        Returns:
            str: The string ''"Rook"''
        """
        return 'Rook'

    def type(self) -> str:
        """Return the display type of the rook.

        Returns:
            str: The type name ''"Rook"''
        """
        return 'Rook'

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        """Determine whether a move is legal for a rook.

        Args:
            move (Move): The candidate move for the rook.
            board (list[list[ChessPiece]]): The current board state.

        Returns:
            bool: ''True'' if the rook can legally execute the move, ''False'' otherwise.
        """
        if not super().is_valid_move(move, board):
            return False

        dr = move.to_row - move.from_row
        dc = move.to_col - move.from_col

        #if our difference of rows and columns arent 0 then it's not a straight line
        if dr != 0 and dc != 0:
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
