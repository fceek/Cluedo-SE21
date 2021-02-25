from logbook import Logbook

class Player:
    """player involved in the game

    DO NOT use directly, a player should be either Human or Ai
    """
    def __init__(self, name, coordinate):
        self.name = name
        self.cards_in_hand = []
        self.coordinate = coordinate
        self.skipped = False
        self.logbook = Logbook()

    def process_suspect(self):
        """make suspection, Interface, DO NOT implement it directly

        """
        pass

    def process_accuse(self):
        """make accusation, Interface, DO NOT implement it directly

        Same as suspection, but player can choose other rooms.
        """
        pass

    def __repr__(self) -> str:
        return "\n[Name: {self.name}, Start Coordinate: {self.coordinate}]".format(self = self)


class Human(Player):
    def process_suspect(self):
        pass

    def process_accuse(self):
        pass

class Ai(Player):
    def process_suspect(self):
        pass

    def process_accuse(self):
        pass