from enum import Enum
from player import Player
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from move import Move

class AI:
    def __init__(self, player: Player) -> None:
        self.__player = player
        self.__opponent = Player.BLACK if player == Player.WHITE else player.WHITE
        self._piece_values = {
            'Pawn': 1,
            'Knight': 3,
            'Bishop': 3,
            'Rook': 5,
            'Queen': 9,
            'King': 1000
        }

    def try_move(self):
        for row in self.board:
            for col in self.board:
                legal, code = self._assess_move(row, col)
                if legal:
                    if self.piece == Pawn:
                        if Pawn.is_valid_move(self.move(row, col, row+2,col+2), self.board):
                            self.piece[row][col] = self.piece[row+2][col+2]
                        else:
                            self.piece[row][col] = self.piece[row+1][col+1]
                    elif self.piece = Knight:
                        if Knight.is_valid_move(move,board):
                            self.piece[row][col] = self.piece[new_row][new_col]
                    #continue with the rest of the pieces
                    else:
                        pass
                elif legal == StayingInCheck:
                    #if we are in check and the current move we are
                    #looking at would still keep us in check then we have to continue to find another move.
                    continue
                elif legal == Invalid:
                    #probably would happen if our move would take us out of bounds.
                    continue
                else:
                    #this would mean that we are moving into check
                    pass



class MoveValidity(Enum):
    """Enumeration describing the result of validating a potential move.

    Attributes:
        Valid (MoveValidity): Indicates the move satisfies all legality checks.
        Invalid (MoveValidity): Indicates the move violates base legality checks
        MovingIntoCheck (MoveValidity): Indicates the move would leave the king in check.
        StayingInCheck (MoveValidity): Indicates the move fails to escape an existing check.
    """
    Valid = 1
    Invalid = 2
    MovingIntoCheck = 3
    StayingInCheck = 4

    def __str__(self):
        """Return a readable message for the move status.

        Returns:
            str: The descriptive message associated with the enum value.
        """
        if self.value == 2:
            return 'Invalid move.'

        if self.value == 3:
            return 'Invalid -- cannot move into check.'

        if self.value == 4:
            return 'Invalid -- must move out of check.'

class UndoException(Exception):
    """Exception raised when an undo operation cannot be performed.

    Attributes:
        message (str): Explanation of why the undo failed.
    """

    def __init__(self, message: str):
        """Initializes a new instance for the UndoException instance.

        Args:
            message (str): Explanation of why the undo failed.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Returns the exception in a readable format for the user.

        Returns:
            message (str): The stored error message.
        """

        return self.message

class ChessModel:
    """Game Engine responsible for move validation, execution, and status.

    Attributes:
        board (list[list[ChessPiece | None]]): Active pieces arranged by board square.
        __message_code (MoveValidity): Outcome of the most recent validiation.
        __ncols (int): Number of columns on the chess board.
        __nrows (int): Number of rows on the chess board.
    """
    def __init__(self):
        """Initialize a new chess model with the standard setup."""
        self.__player = Player.WHITE
        self.__nrows = 8
        self.__ncols = 8
        self.__message_code = MoveValidity.Valid
        self.__move_history: list[dict] = []

        #initialize board
        self.board = [[None] * self.__ncols for _ in range(self.__nrows)]
        self.initialize_board()

    #Read Only Properties
    @property
    def nrows(self) -> int:
        """int: Number of rows on the chess board."""
        return self.__nrows

    @property
    def ncols(self) -> int:
        """int: Number of columns on the chess board."""
        return self.__ncols

    @property
    def current_player(self) -> Player:
        """Player: The player whose turn it is to move."""
        return self.__player

    @property
    def message_code(self) -> MoveValidity:
        """MoveValidity: Outcome of the most recent move validation."""
        return self.__message_code

    #start of our ChessModel main methods
    def is_complete(self) -> bool:
        """Determine whether the current player has any legal moves remaining.

        Returns:
            bool: ''True'' if the game is over (checkmate or stalemate), ''False'' otherwise.
        """
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
        """Validate a move request at the game level.

        Args:
            move (Move): The proposed move.

        Returns:
            bool: ''True'' if the move is legal, ''False'' otherwise.
        """
        legal, code = self._assess_move(move)
        self.__message_code = code
        return legal

    def move(self, move: Move):
        """Execute a move if it is valid and update game state.

        Args:
            move (Move): The move to execute.

        Returns:
            bool: ''True'' if the move was performed, ''False'' otherwise.
        """
        legal, code = self._assess_move(move)
        self.__message_code = code

        if not legal:
            return False

        piece = self.board[move.from_row][move.from_col]
        captured_piece = self.board[move.to_row][move.to_col]
        piece_snapshot = self._snapshot_piece_state(piece)

        history_entry = {
            'move': move,
            'piece': piece,
            'captured': captured_piece,
            'piece_snapshot': piece_snapshot,
            'player_before': self.__player,
            'promotion': False,
        }
        self.board[move.from_row][move.from_col] = None

        if isinstance(piece, Pawn):
            piece.first_move = False
            if (piece.player == Player.WHITE and move.to_row == 0) or (
                piece.player == Player.BLACK and move.to_row == self.__nrows - 1
            ):
                self.board[move.to_row][move.to_col] = Queen(piece.player)
                history_entry['promotion'] = True
            else:
                self.board[move.to_row][move.to_col] = piece
        else:
            self.board[move.to_row][move.to_col] = piece

        self.__move_history.append(history_entry)

        self.set_next_player()
        return True

    def _assess_move(self, move: Move) -> tuple[bool, MoveValidity]:
        """Evaluate a move without mutating persistent state.

        Args:
            move (Move): The move to evaluate.

        Returns:
            tuple[bool, MoveValidity]: Pair of legality flag and explanatory code.
        """
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
        """Capture mutable attributes of a piece for later restoration.

        Args:
            piece (ChessPiece): The piece whose state should be recorded.

        Returns:
            dict: Serialized state needed to undo a move for the piece.
        """
        if isinstance(piece, Pawn):
            return {'first_move': piece.first_move}
        return {}

    def _restore_piece_state(self, piece: ChessPiece, snapshot: dict) -> None:
        """Restore mutable piece attributes from a snapshot.

        Args:
            piece (ChessPiece): The piece whose state should be restored.
            snapshot (dict): The snapshot previously returned by ''_snapshot_piece_state''.
        """
        if isinstance(piece, Pawn) and 'first_move' in snapshot:
            piece.first_move = snapshot['first_move']

    def in_check(self, p: Player):
        """Determine whether the specified player is in check.

        Args:
            p (Player): The player to evaluate.

        Returns:
            bool: ''True'' if the player's king is threatened, ''False'' otherwise.
        """
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
            """Check whether coordinates fall within the board boundaries.

            Args:
                row (int): Row index to validate.
                col (Int): Column index to validate.

            Returns:
                bool: ''True'' if the coordinates are on the board, ''False'' otherwise.
            """
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
        """Retrieve the piece located at the specified coordinates.

        Args:
            row (int): The row index of the target square.
            col (int): The column index of the target square.

        Returns:
            ChessPiece: The piece at the requested position, or ''None'' if empty.

        Raises:
            IndexError: If the coordinates fall outside of the board.
        """
        if not (0 <= row < self.__nrows and 0 <= col < self.__ncols):
            raise IndexError('out of bounds')

        return self.board[row][col]

    def set_next_player(self):
        """Advance the active player to the opponent."""
        self.__player = self.__player.next()

    def set_piece(self, row:int, col:int, piece:ChessPiece):
        """Place a piece on the board at the specified location.

        Args:
            row (int): Target row index.
            col (int): Target column index.
            piece (ChessPiece): The piece to place or ''None'' to clear the square.

        Raises:
            IndexError: If the target square is off the board.
            TypeError: If ''piece'' is not a ''ChessPiece'' or ''None''.
        """
        if not (0 <= row < self.__nrows and 0 <= col < self.__ncols):
            raise IndexError('out of bounds')

        if piece is not None and not isinstance(piece, ChessPiece):
            raise TypeError('piece must be ChessPiece or None')
        self.board[row][col] = piece

    def undo(self):
        """Undo the most recent move.

        Raises:
            UndoException: If there is no move to undo.
        """
        if not self.__move_history:
            raise UndoException('No moves to undo.')

        last_move = self.__move_history.pop()
        move = last_move['move']
        piece = last_move['piece']
        captured_piece = last_move['captured']

        self.board[move.to_row][move.to_col] = captured_piece
        self.board[move.from_row][move.from_col] = piece

        self._restore_piece_state(piece, last_move['piece_snapshot'])
        self.__player = last_move['player_before']
        self.__message_code = MoveValidity.Valid


    def initialize_board(self):
        """Populate the board with the standard chess starting arrangement."""

        #BLACK ROWS
        self.board[0] = [Rook(Player.BLACK), Knight(Player.BLACK), Bishop(Player.BLACK), Queen(Player.BLACK),
                         King(Player.BLACK), Bishop(Player.BLACK), Knight(Player.BLACK), Rook(Player.BLACK)]
        self.board[1] = [Pawn(Player.BLACK) for col in range(self.ncols)]


        #WHITE ROWS
        self.board[7] = [Rook(Player.WHITE), Knight(Player.WHITE), Bishop(Player.WHITE), Queen(Player.WHITE),
                         King(Player.WHITE), Bishop(Player.WHITE), Knight(Player.WHITE), Rook(Player.WHITE)]
        self.board[6] = [Pawn(Player.WHITE) for col in range(self.ncols)]