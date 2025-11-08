from enum import Enum
from player import Player
from move import Move
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from move import Move

class MoveValidity(Enum):
    Valid = 1
    Invalid = 2
    MovingIntoCheck = 3
    StayingInCheck = 4

    def __str__(self):
        if self.value == 2:
            return 'Invalid move.'

        if self.value == 3:
            return 'Invalid -- cannot move into check.'

        if self.value == 4:
            return 'Invalid -- must move out of check.'


# TODO: create UndoException
class UndoException(Exception):
    pass

class ChessModel:
    def __init__(self):
        self.__player = Player.BLACK
        self.__nrows = 8
        self.__ncols = 8
        self.__message_code = MoveValidity.Valid

        #initialize board
        self.board = [[None] * self.__ncols for _ in range(self.__nrows)]
        self.initialize_board()
    #Read Only Properties
    @property
    def nrows(self) -> int:
        return self.__nrows

    @property
    def ncols(self) -> int:
        return self.__ncols

    @property
    def current_player(self) -> Player:
        return self.__player

    @property
    def message_code(self) -> MoveValidity:
        return self.__message_code

    #start of our ChessModel main methods
    def is_complete(self) -> bool:
        #The game is complete if the current player has no legal move (checkmate or stalemate).
        pass
    def is_valid_move(self, move: Move) -> bool:
        # game level move logic, setting the __message_code for each check
        if not ChessPiece.is_valid_move(move, self.board):
            self.__message_code = MoveValidity.Invalid
            return False

        #logic for seeing if move will put in check
        return True

    def move(self, move: Move):
        #actually execute the move if its valid
        pass
        if not ChessModel.is_valid_move:
            self.__message_code = MoveValidity.Invalid
            return False
        #self.board[move.from_row][move.from_col] =
    def in_check(self, p: Player):
        #return true if our players king is currently being attacked by any opponent piece
        pass
    def piece_at(self, row: int, col: int) -> ChessPiece:
        #given a row and a column return the piece if it's at that pos
        pass
        '''
        if self.board[row][col] is not None:
            return self.board[row][col]
        '''

    def set_next_player(self):
        #set the next player
        if self.player == Player.WHITE:
            self.player = Player.BLACK
        else:
            self.player = Player.WHITE
    def set_piece(self, row:int, col:int, piece:ChessPiece):
        #set our piece??
        pass
    def undo(self):
        #undo the most recent move.
        pass

    def initialize_board(self):
        #put all the pieces into their places on the board

        #do the first row
        self.board[0] = [Rook(Player.BLACK), Knight(Player.BLACK), Bishop(Player.BLACK), King(Player.BLACK), Queen(Player.BLACK), Bishop(Player.BLACK), Knight(Player.BLACK), Rook(Player.BLACK)]
        #second row
        #self.board[1] = [Rook(Player.BLACK) for i in range(7)]






