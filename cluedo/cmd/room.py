class Room:
    """rooms in the gameboard
    """
    def __init__(self, name, entrance):
        self.name = name
        self.entrance = entrance

    def __repr__(self) -> str:
        return "\n[Name: {self.name}, Door Coordinate(s): {self.entrance}]".format(self = self)