from cluedo.cmd.logbook import Logbook
from cluedo.cmd.card import Card
import random


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

        self.in_room = None

    def process_suspect(self, cards,target_room) -> dict:
        """make suspection, Interface, DO NOT implement it directly

        """
        pass


    def process_accuse(self) -> dict:
        """make accusation, Interface, DO NOT implement it directly

        Same as suspection, but player can choose other rooms.
        """
        pass

    def selected_card(self,exist) -> dict:
        """make accusation, Interface, DO NOT implement it directly

        Same as suspection, but player can choose other rooms.
        """
        pass

    def __repr__(self) -> str:
        return "\n[Name: {self.name}, Start Coordinate: {self.coordinate}]".format(self = self)


class Human(Player):

    def process_suspect(self, cards,target_room):
        weapon_card = cards['weapons'][int(input('choose weapn: ')) - 1]
        print(weapon_card)
        token_card = cards['tokens'][int(input('choose token: ')) - 1]
        print(token_card)
        return {'weapon': weapon_card, 'token': token_card, 'room': target_room}

    def process_accuse(self, cards):
        if input('Do you want to accuse? Y/N') == 'Y':
            weapon_card = cards['weapons'][int(input('choose weapn: ')) - 1]
            print(weapon_card)
            token_card = cards['tokens'][int(input('choose token: ')) - 1]
            print(token_card)
            room_card = cards['rooms'][int(input('choose room: ')) - 1]
            print(token_card)
            return {'weapon': weapon_card, 'token': token_card, 'room': room_card}

        else:
            return

    def selected_card(self,exist):
        for key, value in exist.items():
            print(key + " : " + str(value)) # show all cards
        print(exist[input('Choose a card to show')]) # show selected card


class Ai(Player):
    """Not really an Ai, all he can do is show you random cards when he can

    """
    def process_suspect(self, cards,target_room):
        weapon_card = cards['weapons'][int(input('choose weapn: ')) - 1]
        print(weapon_card)
        token_card = cards['tokens'][int(input('choose token: ')) - 1]
        print(token_card)
        return {'weapon': weapon_card, 'token': token_card,'room':target_room}

    def process_accuse(self,cards):
        if input('Do you want to accuse? Y/N') == 'Y' or 'y':
            weapon_card = cards['weapons'][int(input('choose weapn: ')) - 1]
            print(weapon_card)
            token_card = cards['tokens'][int(input('choose token: ')) - 1]
            print(token_card)
            room_card = cards['rooms'][int(input('choose room: ')) - 1]
            print(token_card)
            return {'weapon': weapon_card, 'token': token_card, 'room': room_card}
        else:
            return

    def selected_card(self,exist) -> Card:
        """Ai will selected card to show in random

        Args:
            exist (list): cards to choose from

        Returns:
            Card: the card selected by Ai
        """
        return random.choice(list(exist.items()))    # show selected card
