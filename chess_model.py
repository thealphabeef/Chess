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
        for r in range(self.__nrows):
            for c in range(self.__ncols):
                piece = self.board[r][c]
                if piece is None or piece.player != self.__player:
                    continue

                for tr in range(self.__nrows):
                    for tc in range(self.__ncols):
                        piece = self.board[r][c]
                        if piece is None or piece.player != self.__player:
                            continue

                        for tr in range(self.__nrows):
                            for tc in range(self.__ncols):
                                if r == tr and c == tc:
                                    continue

                                potential_move = Move(r,c,tr,tc)
                                legal, _ = self._assess_move(potential_move)
                                if legal:
                                    return False
        return True

    def is_valid_move(self, move: Move) -> bool:
        # game level move logic, setting the __message_code for each check
        legal, code = self._assess_move(move)
        self.__message_code = code
        return legal

    def move(self, move: Move):
        #actually execute the move if its valid
        legal, code = self._assess_move(move)
        self.__message_code = code

        if not legal:
            return False

        piece = self.board[move.from_row][move.from_col]
        self.board[move.from_row][move.from_col] = None
        self.board[move.to_row][move.to_col] = piece

        if isinstance(piece, Pawn):
            piece.first_move = False

        self.set_next_player()
        return True

    def _assess_move(self, move: Move) -> tuple[bool, MoveValidity]:
        fr, fc, tr, tc = move.from_row, move.from_col, move.to_row, move.to_col

        if not (0 <= fr < self.__nrows and 0 <= fc < self.__ncols and
                0 <= tr < self.__nrows and 0 <= tc < self.__ncols):
            return False, MoveValidity.Invalid

        piece = self.board[fr][fc]
        if piece is None or piece.player != self.__player:
            return False, MoveValidity.Invalid

        captured_piece = self.board[tr][tc]

        snapshot = self._snapshot_piece_state(piece)
        if not piece.is_valid_move(move, self.board):
            self._restore_piece_state(piece, snapshot)
            return False, MoveValidity.Invalid
        self._restore_piece_state(piece, snapshot)

        currently_in_check = self.in_check(piece.player)

        self.board[fr][fc] = None
        self.board[tr][tc] = piece
        still_in_check = self.in_check(piece.player)
        self.board[fr][fc] = piece
        self.board[tr][tc] = captured_piece

        if still_in_check:
            if currently_in_check:
                return False, MoveValidity.StayingInCheck
            return False, MoveValidity.MovingIntoCheck
        return True, MoveValidity.Valid


    def _snapshot_piece_state(self, piece: ChessPiece) -> dict:
        if isinstance(piece, Pawn):
            return {'first_move': piece.first_move}
        return {}

    def _restore_piece_state(self, piece: ChessPiece, snapshot: dict) -> None:
        if isinstance(piece, Pawn) and 'first_move' in snapshot:
            piece.first_move = snapshot['first_move']
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
        if not (0 <= row < self.__nrows and 0 <= col < self.__ncols):
            raise IndexError('out of bounds')

        return self.board[row][col]

    def set_next_player(self):
        #set the next player
        self.__player = self.__player.next()

    def set_piece(self, row:int, col:int, piece:ChessPiece):
        #set our piece
        if not (0 <= row < self.__nrows and 0 <= col < self.__ncols):
            raise IndexError('out of bounds')

        if piece is not None and not isinstance(piece, ChessPiece):
            raise TypeError('piece must be ChessPiece or None')
        self.board[row][col] = piece

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






