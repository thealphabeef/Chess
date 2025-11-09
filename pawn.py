from chess_piece import ChessPiece
from move import Move
from player import Player

class Pawn(ChessPiece):
    def __init__(self, player: Player, first_move: bool = True):
        """Initialize a pawn chess piece.

        Args:
            player (Player): Owner of the bishop.
            first_move (bool): Whether the pawn has moved. before. Defaults to True.
        """
        super().__init__(player)
        self.first_move = first_move

    def __str__(self) -> str:
        """Returns the readable name of the pawn.

        Returns:
            str: The string ''"Pawn"''
        """
        return "Pawn"

    def type(self) -> str:
        """Return the display type for the pawn.

        Returns:
            str: The type name ''"Pawn"''
        """
        return "Pawn"

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        """Determine whether a move is legal for a pawn.

        Args:
            move (Move): The candidate move for the pawn.
            board (list[list[ChessPiece]]): The current board state.

        Returns:
            bool: ''True'' if the pawn can legally execute the move, ''False'' otherwise.
        """
        if not super().is_valid_move(move, board):
            return False

        dr = move.to_row - move.from_row
        dc = move.to_col - move.from_col

        direction = -1 if self.player == Player.WHITE else 1 #white goes down and black goes up
        dest_piece = board[move.to_row][move.to_col]

        #forward moves
        if dc == 0:
            if dest_piece is not None: #pawn cant go into occupied square
                return False

            #moving 1 square forward
            if dr == direction:
                self.first_move = False
                return True

            #2 squares forward only if its pawns first move and path is clear
            if self.first_move and dr == 2 * direction:
                mid_row = move.from_row + direction
                if board[mid_row][move.from_col] is None:
                    self.first_move = False
                    return True
            return False

        #diagonal capture
        if abs(dc) == 1 and dr == direction:
            if dest_piece is not None and dest_piece.player != self.player:
                self.first_move = False
                return True

        #just a catch all
        return False
