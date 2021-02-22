"""Development sample for cmd-cluedo

Blueprint for game prototype, subject to change
"""

class Cluedo_Dev:
    """Game main entrance **development version**
    """
    @staticmethod
    def run():
        print("Enter number of players (2-6):")
        player_count = 0
        while not (player_count >= 2 and player_count <= 6):
            try:
                player_count = int(input())
            except:
                print("Please enter a valid number of players")
            else:
                if player_count < 2 or player_count > 6:
                    print("Please enter a valid number of players")
        print("Start game with {} players".format(player_count))
        CluedoGame(player_count)


class CluedoGame:
    """Single round of cluedo game

    Attributes:
        players (list): -
        gameboard (gameboard): -
        cards (list): -
        next_player_iter: iterable object to keep track on player's turns
        next_player: next player to process turn # may redundant
    """

    def __init__(self, player_count):
        """init

        Args:
            player_count (int): number of players in this game
        """
        self.players = []
        self.gameboard = GameBoard()
        self.cards = []

        self.load_gameboard()
        self.load_cards()
        self.load_players(player_count)

        self.generate_answer()
        self.deal_card()

        self.next_player_iter = iter(self.players)
        self.next_player = next(self.next_player_iter)
        while self.process_turn(self.next_player):
            print("Process to next turn")
            pass
        print("Game Ends")

    def process_turn(self, player) -> bool:
        """Process one single turn of the game

        Args:
            player (player): current player operating in this turn

        Returns:
            bool: True if next turn is needed, False if the game is over
        """
        self.display_info()
        move_points = self.roll_dice()
        reachable_rooms = self.gameboard.check_reachable_rooms(player, move_points)

        print(reachable_rooms) # need some formatting
        print("Choose a room to enter:")
        target_room = str(input())
        self.gameboard.move_player_to_room(player, target_room)

        self.process_suspect()
        
        print("Want to accuse? Y/N")
        if str(input()) == "Y":
            if self.process_accuse():
                return False
            else:
                player.skipped = True

        candidate_next = next(self.next_player_iter)
        while candidate_next.skipped:
            candidate_next = next(self.next_player_iter)  # will need to resolve looping
        self.next_player = candidate_next
        return True
        

    def load_gameboard(self):
        """load gameboard setup from external file
        """
        pass

    def load_cards(self):
        """load cards information from external file
        """
        pass

    def load_players(self, player_count):
        """load player information from external file

        Args:
            player_count (int): number of players
        """
        pass

    def generate_answer(self):
        """choose one card of each type to be the correct answer
        """
        pass

    def deal_card(self):
        """deal non-answer cards to players
        """
        pass

    def display_info(self):
        """show essential info that the player need before move in a turn
        """
        pass

    def roll_dice(self) -> int:
        """roll dice to decide move points

        Returns:
            int: roll result
        """
        pass

    def process_suspect(self):
        """make suspection

        This one is rather complicated, player should choose a character and a weapon, while the room be the one player is in.
        Loop through the player list, choose and display card.
        # May need to duplicate player list to avoid interrupt next_player_iter?
        """
        pass

    def process_accuse(self) -> bool:
        """make accusation

        Same as suspection, but player can choose other rooms.

        Returns:
            bool: True if accuse succeed, game over. False if accuse failed, player would be marked as skipped (can't process turn)
        """
        pass

class Card:
    """card indicating informations in the game

    Attributes:
        category (str?): falls in one of ["character", "weapon", "room"]
        description (str): name of the card, no idea why I chose such long name
        is_answer (bool): is this card one of the correct answer cards
    """
    def __init__(self, category, description):
        self.category = category
        self.description = description
        self.is_answer = False

    def make_answer(self):
        self.is_answer = not self.is_answer


class GameBoard:
    """gameboard for players to move on

    Where I really need some other brilliant minds to work together on
    """
    def __init__(self):
        self.board = []
        self.rooms = []

    def check_reachable_rooms(self, player, move_points) -> list:
        pass

    def move_player_to_room(self, player, room):
        pass

    def move_player_to_coordinate(self, player, coord):
        pass


class Room:
    """rooms in the gameboard
    """
    def __init__(self, name, entrance):
        self.name = name
        self.entrance = entrance


class Player:
    """player involved in the game
    """
    def __init__(self, name, coordinate):
        self.name = name
        self.cards_in_hand = []
        self.coordinate = coordinate
        self.skipped = False
