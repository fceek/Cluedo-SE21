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
        dir = os.path.dirname(__file__)    # resolve relative path
        self.setup = self.load_setup(os.path.join(dir,DEFAULT_SETUP))

        self.load_gameboard()
        self.load_cards()
        self.load_players(player_count)

        self.generate_answer()
        self.deal_card()

        self.next_player = 0
        while self.process_turn(self.players[self.next_player]):
           print("Process to next turn")
        print("Game Ends")

    def process_turn(self, player) -> bool:
        """Process one single turn of the game

        Args:
            player (player): current player operating in this turn

        Returns:
            bool: True if next turn is needed, False if the game is over
        """

        move_points = self.roll_dice()
        print(self.cards)
        # print(type(self.cards))
        # for card in self.cards["token"]:
        #     # if card['token'].is_answer:
        #     #     print(str(card['token'])+' is a answer card')
        #     # if card['weapon'].is_answer:
        #     #     print(str(card['weapon']) + ' is a answer card')
        #     # if card['room'].is_answer:
        #     #     print(card['room']+' is a answer card')
        #     print(str(card))

        reachable_rooms = self.gameboard.check_reachable_rooms(player, move_points)
        self.display_info(player, move_points, reachable_rooms)
        #target_room = self.cards['rooms'][int(input('choose a target room: ')) - 1]
        #target_room = reachable_rooms[int(input('choose a room to go'))]
        if len(reachable_rooms) != 0 :
            target_room = self.cards['rooms'][int(input('               Choose a Trget Room:         ')) - 1]
            print('-------------------------------------------------')
            print('           You Choose to Go to Room ↓')
            print(target_room)
            print('-------------------------------------------------')
            self.gameboard.move_player_to_room(player, target_room)

            suspect = player.process_suspect(self.cards, target_room)
            self.check_suspect(suspect, player)
        else:
            print("you have no where to go")
            a=input()



        
        accuse = player.process_accuse(self.cards)
        if accuse:
            #print(self.check_accuse(accuse))
            if self.check_accuse(accuse):
                print('-------------------------------------------------')
                print('Player' + str(player))
                print('          Your Final Accuse is Correct')
                print('           ！！！You Win The Game！！!')
                print('-------------------------------------------------')
                print('-------------------------------------------------')
                print('                    Game END')
                print('-------------------------------------------------')
                return False
            else:
                print('-------------------------------------------------')
                print('           Sorry Your Accuse Is Wrong')
                print('               YOU LOST THE GAME')
                print('-------------------------------------------------')
                print('               Round to continue')
                print('Player'+str(player))
                print('                Out of The Game')
                print('-------------------------------------------------')
                player.skipped = True

        self.next_player = (self.next_player + 1)%len(self.players)
        while self.players[self.next_player].skipped:
            self.next_player = (self.next_player + 1)%len(self.players)  # will need to resolve looping


        return True

    def load_setup(self, path = DEFAULT_SETUP):
        """Load setup JSON from external file

        Args:
            path (string, optional): relative path to setup file. Defaults to DEFAULT_SETUP.

        Returns:
            dict: the unwrapped JSON dict
        """
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

    # TODO()
    def register_logbooks(self):
        """Generate Logbook for each player and do the init
        """
        for this_player in self.players:
            pass

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

    def roll_dice(self) -> int:
        """roll dice to decide move points

        Returns:
            int: roll result
        """
        return random.randint(1,6) + random.randint(1,6)
    
    # TODO()
    def display_info(self,player,move_points,reachable_rooms):
        """show essential info that the player need before move in a turn
        """
        print('--------------------GAME START-------------------')
        print('               Start With ' + str(self.player_count) + ' Players      ')
        print('-------------------------------------------------')
        print('Your are player ↓   Your starting position is ↓ ,' + str(player))
        print('-------------------------------------------------')
        print('            You Got Those Cards In Hand\n' + str(player.cards_in_hand))
        print('-------------------------------------------------')
        print("                   You Can Move \n                        " + str(
            move_points) + "\n                      steps")
        print('-------------------------------------------------')
        print("            You Can Reach Those Rooms \n" + str(reachable_rooms))  # need some formatting
        print('-------------------------------------------------')

    def check_suspect(self, suspect, current_player):
        """Check and response to player suspection

        Args:
            suspect (dict): the suspection, consists of token, weapon and room
        """

        i = self.players.index(current_player) + 1
        while i != self.players.index(current_player):
            exist = {}  # next player empty the selection dict

            if i > len(self.players)-1:
                i = 0
            else:
                if suspect['weapon'] in self.players[i].cards_in_hand:
                    exist['weapon'] = suspect['weapon']
                if suspect['token'] in self.players[i].cards_in_hand:
                    exist['token'] = suspect['token']
                if suspect['room'] in self.players[i].cards_in_hand:
                    exist['room'] = suspect['room']
                if len(exist) != 0:
                    print('Your are player ↓   Your starting position is ↓ ,' + str(self.players[i])+'\n')
                    print('----Because the Current Player is Suspect----\n---------------Your Hand Correctly--------------')

                    print("------So You Need to Show Current Player------")
                    print("---------------One of This Cards--------------")
                    print('-------------------------------------------------')
                    self.players[i].selected_card(exist)    # next player select card to show current player
                    print('-------------------------------------------------')
                i += 1

    def check_accuse(self, accuse):
        """Check and response to player accusation

        Args:
            accuse (dict): the accusation, consists of token, weapon and room
        """
        if accuse['token'].is_answer and accuse['weapon'].is_answer and accuse['room'].is_answer:
            return True
        else:
            return False
        
    def notify_logbooks(self, info):
        """Update all logbook with the info just got

        This might be called in check_suspect(), is an accusation visible to other players?

        Args:
            info (not determined): information from an suspection
        """
        for this_player in self.players:
            this_player.logbook.update(info)
