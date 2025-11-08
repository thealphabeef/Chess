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
        self.__player = Player.WHITE
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
        king_position = None

        #locate king for the current player
        for r in range(self.__nrows):
            for c in range(self.__ncols):
                piece = self.board[r][c]
                if isinstance(piece, King) and piece.player == p:
                    king_position = (r, c)
                    break
            if king_position is not None:
                break
        if king_position is None:
            return False

        #local method for our movement checks so that they dont check off screen
        def on_board(row: int, col: int) -> bool:
            return 0 <= row < self.__nrows and 0 <= col < self.__ncols

        #check every opponent piece to see if it can attack the king :D
        for r in range(self.__nrows):
            for c in range(self.__ncols):
                piece = self.board[r][c]
                if piece is None or piece.player == p: # if we find an empty piece or our own piece go next iter
                    continue

                #pawn possible attacks
                if isinstance(piece, Pawn):
                    direction = -1 if piece.player == Player.WHITE else 1
                    for dc in (-1, 1):
                        attack_row = r + direction
                        attack_col = c + dc
                        if (attack_row, attack_col) == king_position:
                            return True

                #knight possible attacks
                elif isinstance(piece, Knight):
                    #every single possible knight movement lol, could prob be made better??
                    for dr, dc in ((2,1), (1,2), (-1,2), (-2,1),
                                   (-2,-1), (-1,-2), (1,-2), (2,-1)):
                        if (r+dr, c+dc) == king_position:
                            return True

                #bishop or queen's diagonal attacks
                elif isinstance(piece, (Bishop, Queen)):
                    for dr, dc in ((1,1), (1,-1), (-1,1), (-1,-1)):
                        nr, nc = r + dr, c + dc
                        while on_board(nr,nc): # check every tile diagonally
                            target = self.board[nr][nc]
                            if (nr, nc) == king_position: #if we are checking a tile with a king, then its check
                                return True
                            if target is not None: #if theres another piece on the tile it cant be a king then
                                break
                            #keep iterating through tiles
                            nr += dr
                            nc += dc

                #rook our queen's straight attacks
                if isinstance(piece, (Rook, Queen)):
                    for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                        nr, nc = r + dr, c + dc
                        while on_board(nr, nc):  # check every tile straight
                            target = self.board[nr][nc]
                            if (nr, nc) == king_position:  # if we are checking a tile with a king, then its check
                                return True
                            if target is not None:  # if theres another piece on the tile it cant be a king then
                                break
                            # keep iterating through tiles
                            nr += dr
                            nc += dc

                #enemy king adjacent
                if isinstance(piece, King):
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            if (r+dr, c+dc) == king_position:
                                return True
        return False

    def piece_at(self, row: int, col: int) -> ChessPiece:
        #given a row and a column return the piece if it's at that pos
        return self.board[row][col]

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

        #BLACK ROWS
        self.board[0] = [Rook(Player.BLACK), Knight(Player.BLACK), Bishop(Player.BLACK), Queen(Player.BLACK),
                         King(Player.BLACK), Bishop(Player.BLACK), Knight(Player.BLACK), Rook(Player.BLACK)]
        self.board[1] = [Pawn(Player.BLACK) for col in range(self.ncols)]


        #WHITE ROWS
        self.board[7] = [Rook(Player.WHITE), Knight(Player.WHITE), Bishop(Player.WHITE), Queen(Player.WHITE),
                         King(Player.WHITE), Bishop(Player.WHITE), Knight(Player.WHITE), Rook(Player.WHITE)]
        self.board[6] = [Pawn(Player.WHITE) for col in range(self.ncols)]






