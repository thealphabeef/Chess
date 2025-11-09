from enum import Enum

class Player(Enum):
    BLACK = 0
    WHITE = 1

    def next(self):
        """Return the opposing player.

        Returns:
            Player: The next player in turn order.
        """
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

