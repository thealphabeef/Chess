import unittest

from bishop import Bishop
from chess_model import ChessModel, MoveValidity, UndoException
from chess_piece import ChessPiece
from king import King
from knight import Knight
from move import Move
from pawn import Pawn
from player import Player
from queen import Queen
from rook import Rook

#helper methods
class DummyPiece(ChessPiece):
    """simple implementation of the base class."""

    def __str__(self) -> str:
        return 'Dummy'

    def type(self) -> str:
        return 'Dummy'

def make_board(rows: int = 8, cols: int = 8):
    """create an empty board initalized with None in each square."""

    return [[None for _ in range(cols)] for _ in range(rows)]

#base tests
class ChessPieceBaseTests(unittest.TestCase):
    """Shared base beahviour used by all chess peices."""

    def test_base_constraints(self):
        board = make_board()
        piece = DummyPiece(Player.WHITE)
        board[0][0] = piece

        self.assertFalse(piece.is_valid_move(Move(0,0,-1,0), board))#out of bounds
        self.assertFalse(piece.is_valid_move(Move(0,0,0,0), board))#same square
        self.assertFalse(piece.is_valid_move(Move(1,1,1,2), board)) #square that does not have the peice

        friendly = DummyPiece(Player.WHITE)
        board[0][1] = friendly
        self.assertFalse(piece.is_valid_move(Move(0,0,0,1), board)) #moving to a square with friendly piece

        board[0][1] = DummyPiece(Player.BLACK)
        self.assertTrue(piece.is_valid_move(Move(0,0,0,1), board))#moving to empty square owned by opponent

class MoveAndPlayerTests(unittest.TestCase):
    """test move and the nextplayer"""

    def test_move_string_representation(self):
        move = Move(1,2,3,4)
        self.assertEqual(str(move), "Move [from_row=1, from_col=2, to_row=3, to_col=4]")

    def test_player_cycle(self):
        self.assertEqual(Player.WHITE.next(), Player.BLACK)
        self.assertEqual(Player.BLACK.next(), Player.WHITE)

#piece tests
class PawnTests(unittest.TestCase):
    """validate the pawn movement."""

    def test_pawn_first_and_subseqeunt_moves(self):
        board = make_board()
        pawn = Pawn(Player.WHITE)
        board[6][4] = pawn

        self.assertTrue(pawn.is_valid_move(Move(6,4,5,4), board))#white pawns move up
        self.assertFalse(pawn.first_move) #check first move

        board[5][4] = pawn
        self.assertFalse(pawn.is_valid_move(Move(5,4,3,4), board))#test a second forward move

    def test_pawn_double_step_requires_clear_path(self):
        board = make_board()
        pawn = Pawn(Player.BLACK)
        board[1][3] = pawn
        board[2][3] = DummyPiece(Player.WHITE)
        self.assertFalse(pawn.is_valid_move(Move(1,3,3,3), board)) #if first step is blocked, two step should fail

        board[2][3] = None
        self.assertTrue(pawn.is_valid_move(Move(1,3,3,3), board)) #clearing the path allows the move
        self.assertFalse(pawn.first_move) #check first move


    def test_pawn_captures_diagonally(self):
        board = make_board()
        pawn = Pawn(Player.WHITE)
        board[6][2] = pawn
        self.assertFalse(pawn.is_valid_move(Move(6,2,5,3), board)) #diagonal move without enemy should fail

        board[5][3] = DummyPiece(Player.BLACK)
        self.assertTrue(pawn.is_valid_move(Move(6,2,5,3), board)) #enemy piece on diagonal is valid

        board[5][1] = DummyPiece(Player.WHITE)
        self.assertFalse(pawn.is_valid_move(Move(6,2,5,1), board)) #diagonal with the same player piece should fail

    def test_pawn_cannot_capture_forward(self):
        board = make_board()
        pawn = Pawn(Player.BLACK)
        board[1][1] = pawn
        board[2][1] = DummyPiece(Player.WHITE)
        self.assertFalse(pawn.is_valid_move(Move(1,1,2,1), board)) #pawn cant capture above

class RookTests(unittest.TestCase):
    """Validate movement for the Rook"""

    def test_rook_straight_line_movement(self):
        board = make_board()
        rook = Rook(Player.BLACK)
        board[0][0] = rook

        self.assertTrue(rook.is_valid_move(Move(0,0,5,0), board))#vertical move should succeed

        board[3][0] = DummyPiece(Player.WHITE)
        self.assertFalse(rook.is_valid_move(Move(0,0,6,0), board)) #vertical move with something blocking should fail

        board[3][0] = None
        board[0][7] = DummyPiece(Player.WHITE)
        self.assertTrue(rook.is_valid_move(Move(0,0,0,7), board)) #horizontal capture is valid

    def test_rook_rejects_diagonal(self):
        board = make_board()
        rook = Rook(Player.WHITE)
        board[4][4] = rook
        self.assertFalse(rook.is_valid_move(Move(4,4,5,5), board)) #cannot move diagonally

class BishopTests(unittest.TestCase):
    """movement validation for the bishop."""

    def test_bishop_diagonal_movement(self):
        board = make_board()
        bishop = Bishop(Player.WHITE)
        board[3][3] = bishop

        self.assertTrue(bishop.is_valid_move(Move(3,3,0,0), board)) #diagonal move works

        board[2][2] = DummyPiece(Player.BLACK)
        self.assertFalse(bishop.is_valid_move(Move(3,3,0,0), board)) #adding a blocker on path should fail

        board[2][2] = None
        board[0][6] = DummyPiece(Player.BLACK)
        self.assertTrue(bishop.is_valid_move(Move(3,3,0,6), board)) #capturing a enemy diagonally is valid

    def test_bishop_rejects_straight(self):
        board = make_board()
        bishop = Bishop(Player.BLACK)
        board[2][2] = bishop
        self.assertFalse(bishop.is_valid_move(Move(2,2,2,4), board)) #moving straight shouold fail.

class KnightTests(unittest.TestCase):
    """movement validation for the knight"""

    def test_knight_1_shape_movement(self):
        board = make_board()
        knight = Knight(Player.BLACK)
        board[4][4] = knight

        #all valid L shaped moves should succeed even with intervening pieces.
        board[3][4] = DummyPiece(Player.WHITE)
        self.assertTrue(knight.is_valid_move(Move(4,4,6,5), board))
        self.assertTrue(knight.is_valid_move(Move(4,4,5,6), board))
        self.assertFalse(knight.is_valid_move(Move(4,4,4,6), board))

class QueenTests(unittest.TestCase):
    """movement validation for the queen."""

    def test_queen_combines_rook_and_bishop_movement(self):
        board = make_board()
        queen = Queen(Player.WHITE)
        board[4][4] = queen

        self.assertTrue(queen.is_valid_move(Move(4,4,4,0), board)) #straight move is valid
        self.assertTrue(queen.is_valid_move(Move(4,4,1,1), board)) #diagonal move is valid

        board[2][4] = DummyPiece(Player.BLACK)
        self.assertFalse(queen.is_valid_move(Move(4,4,0,4), board)) #enemy blocking path prevents moves

    def test_queen_invalid_knight_like_move(self):
        board = make_board()
        queen = Queen(Player.BLACK)
        board[0][0] = queen
        self.assertFalse(queen.is_valid_move(Move(0,0,1,2), board)) #cannot move like a knight

class KingTests(unittest.TestCase):
    """movement rules for the king."""

    def test_king_single_square_movement(self):
        board = make_board()
        king = King(Player.BLACK)
        board[4][4] = king

        #adjacent squares are valid destinations.
        self.assertTrue(king.is_valid_move(Move(4,4,5,5), board))
        self.assertTrue(king.is_valid_move(Move(4,4,4,3), board))

        self.assertFalse(king.is_valid_move(Move(4,4,6,4), board)) #move larger than one square should fail

        #capturing an enemy is allowed, but friendly pieces block the destination.
        board[3][3] = DummyPiece(Player.WHITE)
        self.assertTrue(king.is_valid_move(Move(4,4,3,3), board))
        board[5][5] = DummyPiece(Player.BLACK)
        self.assertFalse(king.is_valid_move(Move(4,4,5,5), board))

class ChessModelBoardSetupTests(unittest.TestCase):
    def test_initial_board_configuration(self):
        model = ChessModel()
        self.assertIsInstance(model.board[0][0], Rook)
        self.assertIsInstance(model.board[0][4], King)
        self.assertIsInstance(model.board[1][3], Pawn)
        self.assertIsInstance(model.board[6][5], Pawn)
        self.assertIsInstance(model.board[7][3], Queen)

        self.assertEqual(model.nrows, 8)
        self.assertEqual(model.ncols, 8)

    def test_piece_at_bounds_and_errors(self):
        model = ChessModel()
        self.assertRaises(IndexError, model.piece_at, -1,0)
        self.assertIsInstance(model.piece_at(0,1), Knight)

    def test_set_piece_validation(self):
        model = ChessModel()
        with self.assertRaises(IndexError):
            model.set_piece(9,9, Pawn(Player.WHITE))
        with self.assertRaises(TypeError):
            model.set_piece(0,0, "not a piece")
        dummy = DummyPiece(Player.BLACK)
        model.set_piece(0,0, dummy)
        self.assertIs(model.board[0][0], dummy)

class ChessModelMoveLogicTests(unittest.TestCase):
    def setUp(self):
        self.model = ChessModel()
        #clear the board
        self.model.board = make_board()
        self.model._ChessModel__player = Player.WHITE

    def test_assess_move_restores_pawn_state(self):
        pawn = Pawn(Player.WHITE)
        self.model.board[6][0] = pawn
        legal, code = self.model._assess_move(Move(6,0,4,0))
        self.assertTrue(legal)
        self.assertEqual(code, MoveValidity.Valid)
        self.assertTrue(pawn.first_move)

    def test_move_updates_history_and_switches_player(self):
        self.model.board[6][0] = Pawn(Player.WHITE)
        self.assertTrue(self.model.move(Move(6,0,5,0)))
        self.assertEqual(len(self.model._ChessModel__move_history), 1)
        self.assertEqual(self.model.current_player, Player.BLACK)

    def test_move_rejects_if_invalid_and_sets_message(self):
        self.model.board[7][0] = Rook(Player.WHITE)
        self.model.board[7][7] = Rook(Player.WHITE)
        ok = self.model.move(Move(7,0,7,7))
        self.assertFalse(ok)
        self.assertEqual(self.model.message_code, MoveValidity.Invalid)

    def test_pawn_promotion_to_queen(self):
        pawn = Pawn(Player.WHITE)
        self.model.board[1][0] = pawn
        self.assertTrue(self.model.move(Move(1,0,0,0)))
        promoted_piece = self.model.board[0][0]
        self.assertIsInstance(promoted_piece, Queen)
        self.assertNotEqual(promoted_piece, pawn)

    def test_undo_restores_board_and_player(self):
        pawn = Pawn(Player.WHITE)
        self.model.board[6][0] = pawn
        self.model.move(Move(6,0,5,0))
        self.assertEqual(self.model.current_player, Player.BLACK)
        self.model.undo()
        self.assertEqual(self.model.current_player, Player.WHITE)
        self.assertIs(self.model.board[6][0], pawn)
        self.assertIsNone(self.model.board[5][0])
        self.assertTrue(pawn.first_move)

    def test_undo_without_history_raises(self):
        with self.assertRaises(UndoException):
            self.model.undo()

    def test_in_check_detection(self):
        white_king = King(Player.WHITE)
        self.model.board[7][4] = white_king
        self.model.board[0][4] = Rook(Player.BLACK)
        self.assertTrue(self.model.in_check(Player.WHITE))
        self.assertFalse(self.model.in_check(Player.BLACK))
        self.model.board[7][5] = DummyPiece(Player.BLACK)
        self.assertTrue(self.model.in_check(Player.WHITE))
        self.assertIs(white_king, self.model.board[7][4])

    def test_assess_move_prevents_moving_into_check(self):
        self.model.board[1][2] = King(Player.WHITE)
        self.model.board[0][0] = Rook(Player.BLACK)

        legal, code = self.model._assess_move(Move(1,2,0,2))
        self.assertFalse(legal)
        self.assertEqual(code, MoveValidity.MovingIntoCheck)

    def test_assess_move_detects_staying_in_check(self):
        self.model.board[0][4] = King(Player.WHITE)
        self.model.board[1][4] = Rook(Player.BLACK)
        self.model.board[1][5] = Rook(Player.BLACK)

        legal, code = self.model._assess_move(Move(0,4,0,5))
        self.assertFalse(legal)
        self.assertEqual(code, MoveValidity.StayingInCheck)

    def test_is_complete_true_when_no_pieces(self):
        self.model.board = make_board()
        self.assertTrue(self.model.is_complete())

    def test_is_complete_false_when_legal_move_exists(self):
        self.model.board[7][4] = King(Player.WHITE)
        self.model.board[0][4] = King(Player.BLACK)
        self.assertFalse(self.model.is_complete())

if __name__ == "__main__":
    unittest.main()
