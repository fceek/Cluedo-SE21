class Player:
    """player involved in the game

    DO NOT use directly, a player should be either Human or Ai
    """
    def __init__(self, name, coordinate):
        self.name = name
        self.cards_in_hand = []
        self.coordinate = coordinate
        self.skipped = False

    def process_suspect(self):
        """make suspection, Interface, DO NOT implement it directly

        This one is rather complicated, player should choose a character and a weapon, while the room be the one player is in.
        Loop through the player list, choose and display card.
        # May need to duplicate player list to avoid interrupt next_player_iter?
        """
        pass

    def process_accuse(self) -> bool:
        """make accusation, Interface, DO NOT implement it directly

        Same as suspection, but player can choose other rooms.

        Returns:
            bool: True if accuse succeed, game over. False if accuse failed, player would be marked as skipped (can't process turn)
        """
        pass

    def __repr__(self) -> str:
        return "\n[Name: {self.name}, Start Coordinate: {self.coordinate}]".format(self = self)


class Human(Player):
    def process_suspect(self):
        pass

    def process_accuse(self) -> bool:
        pass

class Ai(Player):
    def process_suspect(self):
        pass

    def process_accuse(self) -> bool:
        pass