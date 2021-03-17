DEFAULT_SETUP = "data/default.json"

from player import Player, Ai, Human
from gameboard import GameBoard
from card import Card
from room import Room

import json, random, os

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
        self.player_count = player_count
        self.players = []
        self.gameboard = GameBoard()
        self.cards = {
            "tokens"    : [],
            "weapons"   : [],
            "rooms"     : []
        }
        dir = os.path.dirname(__file__)
        self.setup = self.load_setup(os.path.join(dir,DEFAULT_SETUP))

        self.load_gameboard()
        self.load_cards()
        self.load_players(player_count)

        self.generate_answer()
        self.deal_card()

        #self.next_player_iter = iter(self.players)
        #self.next_player = next(self.next_player_iter)
        #while self.process_turn(self.next_player):
        #    print("Process to next turn")
        #    pass
        #print("Game Ends")

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

        player.process_suspect()
        
        print("Want to accuse? Y/N")
        if str(input()) == "Y":
            if player.process_accuse():
                return False
            else:
                player.skipped = True

        candidate_next = next(self.next_player_iter)
        while candidate_next.skipped:
            candidate_next = next(self.next_player_iter)  # will need to resolve looping
        self.next_player = candidate_next
        return True
        

    def load_setup(self, path = DEFAULT_SETUP):
        with open(path) as setup_file:
            setup = json.load(setup_file)
        return setup

    def load_gameboard(self):
        """load gameboard setup from external file
        """
        map_setup = self.setup["setup"]["map"]

        self.gameboard.board = map_setup["map_layout"]
        self.gameboard.rooms = []
        for this_room in map_setup["rooms"]:
            self.gameboard.rooms.append(Room(this_room["name"], this_room["doors"]))

    def load_cards(self):
        """load cards information from external file
        """
        for this_token in self.setup["setup"]["tokens"]:
            self.cards["tokens"].append(Card("token", this_token["name"]))
        for this_weapon in self.setup["setup"]["weapons"]:
            self.cards["weapons"].append(Card("weapon", this_weapon))
        for this_room in self.setup["setup"]["map"]["rooms"]:
            self.cards["rooms"].append(Card("room", this_room["name"]))

    def load_players(self, player_count):
        """load player information from external file

        Args:
            player_count (int): number of players
        """
        player_setup = self.setup["setup"]["tokens"].copy()
        random.shuffle(player_setup)
        for i in range(player_count):
            self.players.append(Human(player_setup[i]["name"], player_setup[i]["start"]))

    def generate_answer(self):
        """choose one card of each type to be the correct answer
        """
        random.choice(self.cards["tokens"]).make_answer()
        random.choice(self.cards["weapons"]).make_answer()
        random.choice(self.cards["rooms"]).make_answer()

    def deal_card(self):
        """deal non-answer cards to players
        """
        all_cards_with_answers = (
            self.cards["tokens"]
          + self.cards["weapons"]
          + self.cards["rooms"]
        )
        all_cards = [x for x in all_cards_with_answers if not x.is_answer]
        random.shuffle(all_cards)
        extra_card_num = len(all_cards) % self.player_count
        card_num = len(all_cards) // self.player_count
        for i in range(extra_card_num):
            self.players[i].cards_in_hand = all_cards[
                (card_num + 1) * i
              : (card_num + 1) * (i + 1)
            ]
        for i in range(extra_card_num, self.player_count):
            self.players[i].cards_in_hand = all_cards[
                extra_card_num + card_num * i
              : extra_card_num + card_num * (i + 1)
            ]

    def display_info(self):
        """show essential info that the player need before move in a turn
        """
        pass

    def roll_dice(self) -> int:
        """roll dice to decide move points

        Returns:
            int: roll result
        """
        return random.randint(1,6) + random.randint(1,6)