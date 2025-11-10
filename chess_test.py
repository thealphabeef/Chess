import pytest

from bishop import Bishop
from chess_piece import ChessPiece
from king import King
from knight import Knight
from move import Move
from pawn import Pawn
from player import Player
from queen import Queen
from rook import Rook


class DummyPiece(ChessPiece):
    """Simple concrete implementation of the base class."""

    def __str__(self) -> str:
        return 'Dummy'

    def type(self) -> str:
        return 'Dummy'

def make_board(rows: int = 8, cols: int = 8):
    """Create an empty board initalized with ''None'' in each square."""

    return [[None for _ in range(cols)] for _ in range(rows)]


#CHESS_PIECE BASE CLASS


def test_chess_piece_base_constraints():
    """Ensure the common validations shared by all pieces behave correctly."""

    board = make_board()
    piece = DummyPiece(Player.WHITE)
    board[0][0] = piece

    #Out of bounds coordinates should be rejected.
    assert not piece.is_valid_move(Move(0,0,-1,0), board)

    #Moving to the same square is not considered a valid move.
    assert not piece.is_valid_move(Move(0,0,0,0), board)

    #Moving from a square that does not contain the piece is invalid.
    assert not piece.is_valid_move(Move(1,1,1,2), board)

    #Moving onto a friendly piece should be blocked.
    friendly = DummyPiece(Player.WHITE)
    board[0][1] = friendly
    assert not piece.is_valid_move(Move(0,0,0,1), board)

    #Moving to an empty square owned by the opponent passes the base checks.
    board[0][1] = None
    board[0][1] = DummyPiece(Player.BLACK)
    assert piece.is_valid_move(Move(0,0,0,1), board)


#PAWN


def test_pawn_first_and_subseqeunt_moves():
    """Verify pawn forward moves"""

    board = make_board()
    pawn = Pawn(Player.WHITE)
    board[6][4] = pawn

    #White pawns should move up
    assert pawn.is_valid_move(Move(6,4,5,4), board)
    assert not pawn.first_move

    #After moving once, a second forward move of two squares must fail.
    board[5][4] = pawn
    assert not pawn.is_valid_move(Move(5,4,3,4), board)


def test_pawn_double_step_requires_clear_path():
    """Check that the opening two step move is blocked by intervening piece."""

    board = make_board()
    pawn = Pawn(Player.BLACK)
    board[1][3] = pawn

    #Block the intermediate square, the two step advance should fail.
    board[2][3] = DummyPiece(Player.WHITE)
    assert not pawn.is_valid_move(Move(1,3,3,3), board)

    #Clearing the path allows the move to succeed and toggles ''first_move''.
    board[2][3] = None
    assert pawn.is_valid_move(Move(1,3,3,3), board)
    assert not pawn.first_move


def test_pawn_captures_diagonally():
    """Ensure pawns can capture diagonally but not move diagonally without an enemy."""

    board = make_board()
    pawn = Pawn(Player.WHITE)
    board[6][2] = pawn

    #Diagonal move without an enemy should fail.
    assert not pawn.is_valid_move(Move(6,2,5,3), board)

    #Placing an enemy piece on the diagonal should make the capture valid.
    board[5][3] = DummyPiece(Player.BLACK)
    assert pawn.is_valid_move(Move(6,2,5,3), board)

    #Pawns may not capture pieces belonging to the same player.
    board[5][1] = DummyPiece(Player.WHITE)
    assert not pawn.is_valid_move(Move(6,2,5,1), board)


#ROOK


def test_rook_straight_line_movement():
    """Confirm that rooks move any number of squares in straight lines."""

    board = make_board()
    rook = Rook(Player.BLACK)
    board[0][0] = rook

    #Vertical move should succeed when path is clear.
    assert rook.is_valid_move(Move(0,0,5,0), board)

    #Place an obstruction to confirm the path-blocking logic
    board[3][0] = DummyPiece(Player.WHITE)
    assert not rook.is_valid_move(Move(0,0,6,0), board)

    #Horizontal capture of an opposing piece should be allowed.
    board[3][0] = None
    board[0][7] = DummyPiece(Player.WHITE)
    assert rook.is_valid_move(Move(0,0,0,7), board)


#BISHOP


def test_bishop_diagonal_movement():
    """Validate that bishops move diagonally and stop for blocking pieces."""
    board = make_board()
    bishop = Bishop(Player.WHITE)
    board[3][3] = bishop

    #diagonal move works with an empty path.
    assert bishop.is_valid_move(Move(3,3,0,0), board)

    #adding a blocker along the path shoudl prevent the move.
    board[2][2] = DummyPiece(Player.BLACK)
    assert not bishop.is_valid_move(Move(3,3,0,0), board)

    #capturing a diagonally positioned enemy is valid.
    board[2][2] = None
    board[0][6] = DummyPiece(Player.BLACK)
    assert bishop.is_valid_move(Move(3,3,0,6), board)


#KNIGHT


def test_knight_1_shape_movement():
    """Check that knights move in their correct movement and can jump over pieces."""

    board = make_board()
    knight = Knight(Player.BLACK)
    board[4][4] = knight

    #all valid L shaped moves should succeed even with intervening pieces.
    board[3][4] = DummyPiece(Player.WHITE)
    assert knight.is_valid_move(Move(4,4,6,5), board)
    assert knight.is_valid_move(Move(4,4,5,6), board)
    assert not knight.is_valid_move(Move(4,4,4,6), board)


#QUEEN


def test_queen_combines_rook_and_bishop_movement():
    """Ensure the queen respects both straight and diagonal movement rules."""

    board = make_board()
    queen = Queen(Player.WHITE)
    board[4][4] = queen

    #Straight move behaves like a rook.
    assert queen.is_valid_move(Move(4,4,4,0), board)

    #Diagonal move behaves like a bishop.
    assert queen.is_valid_move(Move(4,4,1,1), board)

    #A blocker should prevent straight-line moves.
    board[2][4] = DummyPiece(Player.BLACK)
    assert not queen.is_valid_move(Move(4,4,0,4), board)


#KING


def test_king_single_square_movement():
    """Confirm that kings move one square in any direction but not further."""

    board = make_board()
    king = King(Player.BLACK)
    board[4][4] = king

    #Adjacent squares are valid destinations.
    assert king.is_valid_move(Move(4,4,5,5), board)
    assert king.is_valid_move(Move(4,4,4,3), board)

    #Moves larger than one square must be rejected.
    assert not king.is_valid_move(Move(4,4,6,4), board)

    #Capturing an enemy is allowed, but friendly pieces block the destination.
    board[3][3] = DummyPiece(Player.WHITE)
    assert king.is_valid_move(Move(4,4,3,3), board)
    board[5][5] = DummyPiece(Player.BLACK)
    assert not king.is_valid_move(Move(4,4,5,5), board)
