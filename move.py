class Move:
    def __init__(self, from_row, from_col, to_row, to_col):
        """Initialize a move description.

        Args:
            from_row (int): Starting index row.
            from_col (int): Starting index column.
            to_row (int): Destination row index.
            to_col (int): Destination column index.
        """
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col

    def __str__(self):
        """Return a readable representation of the move.

        Returns:
            str: String describing the origin and destination squares.
        """
        output = f'Move [from_row={self.from_row}, from_col={self.from_col}'
        output += f', to_row={self.to_row}, to_col={self.to_col}]'
        return output	
