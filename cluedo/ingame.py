"""Cluedo Game GUI Controller

"""

# Kivy imports
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
Config.write()

from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import (
    ScreenManager, Screen, FadeTransition
)
from kivy.properties import StringProperty
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.logger import Logger

# Cluedo cmd imports

from cluedo.cmd.cluedo_game import CluedoGame

Builder.load_file('ingame.kv')

# Widget Components

class Grid_button(Button):
    """Button for Gameboard, used for walkable squares(red border)

    Args:
        btn_x (int): x coordinate of the button
        btn_y (int): y coordinate of the button
    """
    def __init__(self, btn_x, btn_y, **kwargs):
        super().__init__(**kwargs)
        self.btn_x = btn_x
        self.btn_y = btn_y

class Trans_button(Button):
    """Button for Gameboard, used for not walkable squares(invisible)

    Args:
        btn_x (int): x coordinate of the button
        btn_y (int): y coordinate of the button
    """
    def __init__(self, btn_x, btn_y, **kwargs):
        super().__init__(**kwargs)
        self.btn_x = btn_x
        self.btn_y = btn_y

class Card_display(Button):
    """Represent 'cards' of the game

    Args:
        card_type (str): type of the card (token, weapon or room)
        card_name (str): card description
        card_clickable (bool): if the card is display only, or can be clicked to select
    
    Attrs:
        image_source (StringProperty): file path for card image
    """
    image_source = StringProperty('default')
    def __init__(self, card_type, card_name, card_clickable = False, **kwargs):
        super().__init__(**kwargs)
        self.card_type = card_type
        self.card_name = card_name
        self.card_clickable = card_clickable
        self.image_source = 'images/' + card_type + 's/' + card_name + '_Card.png'

class Prev_Btn(Button):
    """The previous button on top

    """
    pass

class Next_Btn(Button):
    """The next button on top

    """
    pass

# App Components

class Main_menu(Screen):
    """Page: Main menu

    """
    pass

class New_game(Screen):
    """Page: New game

    Attrs:
        character_chosen (str): name of the token player selects
        previous_btn: the button player selected previously
        previous_overlay: the 'selected' overlay displayed above previous_btn
    """
    character_chosen = None
    previous_btn = None
    previous_overlay = None

    def choose_character(self, character):
        """Handles player choosing which token want to use in the game

        Args:
            character (str): name of the token selected by player
        """
        #print(self.ids[character])
        self.character_chosen = character
        char_button = self.ids[character + '_btn']
        if self.previous_btn:
            self.previous_btn.remove_widget(self.previous_overlay)
        overlay = Image(source='images/Selected.png')
        overlay.center = char_button.center
        char_button.add_widget(overlay)
        self.previous_btn = char_button
        self.previous_overlay = overlay
    
    def start_game(self):
        """Start a new game if a token is selected

        """
        player_count = self.ids['slider_player_num'].value
        if self.character_chosen:
            self.manager.get_screen('game_body').load_page(player_count, self.character_chosen)
            self.manager.transition = FadeTransition()
            self.manager.current = 'game_body'

class Game_body(Screen):
    """Page: Main game, including gameboard and main information display

    Attrs:
        next_callback (lambda): callback function of 'Next' button
        prev_callback (lambda): callback function of 'Previous' button
        next_btn (Next_btn): the instance of 'Next' button
        prev_btn (Prev_btn): the instance of 'Previous' button

        layer_control (PageLayout): controller to switch between layers
        game_reference (Cluedo_game): command line game at the backend
        gameboard (GridLayout): container of all grid buttons
        info_text (Label): primary information text of the game
    """

    def load_page(self, player_count, character_chosen):
        """Load the gameboard GUI
            
        Callback: 
            process_turn()

        Args:
            player_count (int): number of players of this game in total
            character_chosen (str): name of the token selected by player
        """
        # reset, clear cache
        self.next_callback = None
        self.prev_callback = None
        self.next_btn = self.ids['next_btn']
        self.prev_btn = self.ids['prev_btn']
        if self.next_callback:
            self.next_btn.unbind(on_press = self.next_callback)
        if self.prev_callback:
            self.prev_btn.unbind(on_press = self.prev_callback)
        self.next_btn.background_normal = 'images/Next.png'
        self.prev_btn.background_normal = 'images/Black_Box.png'
        self.layer_control = self.ids['layer_control']
        self.game_reference = CluedoGame(player_count, character_chosen)

        # prepare gameboard display
        size = self.game_reference.setup["setup"]["map"]["size"]
        self.gameboard = self.ids['gameboard']
        self.gameboard.clear_widgets()
        self.info_text = self.ids['basic_info']
        self.gameboard.rows = size[1]
        self.gameboard.cols = size[0]
        Logger.info(self.game_reference.cards)
        for row in range(0, size[1]):
            for col in range(0, size[0]):
                gameboard_data = self.game_reference.gameboard.board[row][col]
                if gameboard_data == 0:
                    self.gameboard.add_widget(Grid_button(row, col))
                else:
                    self.gameboard.add_widget(Trans_button(row, col))
                #gameboard.add_widget(Button(text = str(row) + ',' + str(col)))
        self.info_text.text = 'Playing as [b]' + character_chosen.capitalize() + '[/b]'

        # while character_chosen.capitalize() not in self.game_reference.players[self.game_reference.next_player].name:
        #     self.game_reference.next_player += 1

        self.process_turn(self.game_reference.players[self.game_reference.next_player])

    def process_turn(self, player):
        """Starting a new turn for current player

        Callback:
            display_info()

        Args:
            player (Player): current player in action during this turn
        """
        move_points = self.game_reference.roll_dice()
        backup_move_points = move_points
        reachable_rooms = []
        while len(reachable_rooms) == 0 :
            reachable_rooms = self.game_reference.gameboard.check_reachable_rooms(player, move_points)
            move_points += 1
        if self.next_callback:
            self.next_btn.unbind(on_press = self.next_callback)
        if self.prev_callback:
            self.prev_btn.unbind(on_press = self.prev_callback)
        self.next_callback = lambda root:self.display_info(player, backup_move_points, reachable_rooms)
        self.next_btn.bind(on_press = self.next_callback)
    
    def process_suspect(self, player, cards):
        """Preparing to display 'make suggestion' page for the player to choose

        Callback:
            load_choice()

        Args:
            player (Player): current player in action
            cards (list): list of all cards used in this game
        """
        self.manager.get_screen('player_action').load_choice(2, player)
        self.manager.current = 'player_action'

    def display_info(self, player, move_points, reachable_rooms):
        """Display information of current player, including move points get from the dices, cards in player's hold and possible rooms the player can get in

        Callback:
            to_room_on_press()

        Args:
            player (Player): current player in action
            move_points (int): the step number player can use
            reachable_rooms (list): list of rooms player can enter
        """
        self.layer_control.page = 1
        current_layer = self.ids['player_overlay']
        self.ids['dice_points'].text = '[b]' + str(move_points) + '[/b]'
        hand = self.ids['cards_in_hand']
        hand.clear_widgets()
        for this_card in player.cards_in_hand:
            hand.add_widget(Card_display(this_card.category, this_card.description))
        choose_room = self.ids['rooms_to_go']
        choose_room.clear_widgets()
        for this_room in reachable_rooms:
            btn_callback = lambda root, this_player = player, temp_room = this_room:self.to_room_on_press(this_player, temp_room)
            # btn_callback = partial(self.to_room_on_press, player, this_room)
            this_btn = Button(text = this_room.name,
                              size_hint = (None, None),
                              size = (140, 48),
                              font_size = 20,
                              background_normal = 'images/White_Box.png',
                              background_color = (1, 1, 1, 1),
                              color = (0.7, 0, 0, 1),
                              on_press = btn_callback
            )
            choose_room.add_widget(this_btn)
    
    def to_room_on_press(self, player, room):
        """Handler for player selecting which room to enter

        Callback:
            process_suspect()

        Args:
            player (Player): current player in action
            room (Room): the room player decided to enter
        """
        self.game_reference.gameboard.move_player_to_room(player, room)
        self.info_text.text = player.name + ' has moved to ' + room.name
        self.layer_control.page = 0
        suspect = self.process_suspect(player, self.game_reference.cards)

    def submit_callback(self, action, submission):
        """Process the suggestion or accuse submitted by player

        Callback:
            do_accuse(): after a suggestion, ask for player make an accusation or not
            Game_ending.load_page(): after an accusation, display the result (player will either lose or win)

        Args:
            action (str): 'suspect' for suggestion, 'accuse' for accusation
            submission (dict): the dictionary including token, weapon and room
        """
        # Logger.info('received ')
        # Logger.info(action)
        if action == 'suspect':
            response = self.game_reference.check_suspect(submission, self.game_reference.players[self.game_reference.next_player])
            # Logger.info(response)
            self.manager.current = 'game_body'
            info_str = ''
            for this_response in response:
                key = str(list(this_response.keys())[0])
                value = list(this_response.values())[0]
                # Logger.info(value)
                info_str = (info_str
                        + '[b]' + key + '[/b]'
                        + ' showed you: '
                        + '[b]' + value[1].category.capitalize() + '[/b]'
                        + ', '
                        + '[b]' + value[1].description + '[/b]'
                        + '\n'
                )
            if info_str == '':
                info_str = 'Nobody can help you with your suspect!'
            self.info_text.text = info_str
            self.next_btn.unbind(on_press = self.next_callback)
            self.next_callback = lambda root:self.do_accuse(self.game_reference.cards)
            self.next_btn.bind(on_press = self.next_callback)
        if action == 'accuse':
            response = self.game_reference.check_accuse(submission)
            if response:
                self.manager.get_screen('game_ending').load_page('win', self.game_reference.players[self.game_reference.next_player])
                self.manager.current = 'game_ending'
            else:
                self.manager.get_screen('game_ending').load_page('lose', self.game_reference.players[self.game_reference.next_player])
                self.manager.current = 'game_ending'

    def do_accuse(self, cards):
        """Ask if the player want to make an accusation

        Callback:
            next_turn(): the player do not want an accusation, start a new turn for next player
            process_accuse(): the player choose to make an accusation

        Args:
            cards (list): list of all cards used in this game
        """
        self.info_text.text = 'Do you want to [b]Make Accuse[/b]?'
        self.prev_btn.background_normal = 'images/No_Btn.png'
        if self.prev_callback:
            self.prev_btn.unbind(on_press = self.prev_callback)
        self.prev_callback = lambda root:self.next_turn(self.game_reference.players[self.game_reference.next_player])
        self.prev_btn.bind(on_press = self.prev_callback)

        self.next_btn.background_normal = 'images/Yes_Btn.png'
        # Logger.info(self.next_btn.on_press)
        self.next_btn.unbind(on_press = self.next_callback)
        # Logger.info(self.next_btn.on_press)
        self.next_callback = lambda root, temp_cards = cards:self.process_accuse(temp_cards)
        self.next_btn.bind(on_press =  self.next_callback)
        # Logger.info(self.next_btn.on_press)

    def process_accuse(self, cards):
        """Preparing to display 'make accusation' page for the player to choose

        Callback:
            load_choice()

        Args:
            cards (list): list of all cards used in this game
        """
        self.manager.get_screen('player_action').load_choice(3)
        self.manager.current = 'player_action'

    def next_turn(self, player):
        """Ready for next turn, find next player that can move and clearing cache

        Callback:
            process_turn()

        Args:
            player (Player): current player in action
        """
        the_game = self.game_reference
        the_game.next_player = (the_game.next_player + 1) % len(the_game.players)
        while the_game.players[the_game.next_player].skipped:
            the_game.next_player = (the_game.next_player + 1) % len(the_game.players)
        the_next = the_game.players[the_game.next_player]
        self.info_text.text = 'Playing as [b]' + the_next.name.capitalize() + '[/b]'
        self.next_btn.background_normal = 'images/Next.png'
        self.prev_btn.background_normal = 'images/Black_Box.png'
        self.process_turn(the_next)
        

    def pressed(self, the_button):
        """DEBUG: check which button was pressed

        Args:
            the_button (Button): button got pressed
        """
        pass
        # self.info_text.text = "pressed button @ " + str(the_button.btn_x) + ',' + str(the_button.btn_y)

class Player_action(Screen):
    """Page: player complete suggestion or accusation on this page

    Attrs:
        choice (dict): suggestion or accusation by player
        action (str): indicating the type of submission, 'suspect' for suggestion, 'accuse' for accusation

        game_reference (Cluedo_game): command line game at the backend
        token_empty, weapon_empty, room_empty (Card_display): placeholder slots for the player to fill their choices in
    """
    choice = {'token': None, 'weapon': None, 'room': None}
    action = ''

    def load_choice(self, choice_num, player = None):
        """Preparing the display, load all options from game, so that player can choose from them

        Args:
            choice_num (int): number of choices player need to make, 3 for accusation, 2 for suggestion because room is fixed
            player (Player, optional): current player in action. Defaults to None.
        """
        self.game_reference = self.manager.get_screen('game_body').game_reference
        self.ids['cards_to_choose'].clear_widgets()
        container = self.ids['placeholder_choice']
        container.clear_widgets()
        self.token_empty = Card_display('other', 'empty', True)
        self.token_empty.bind(on_press = lambda root:self.show_cards('tokens'))
        container.add_widget(self.token_empty)
        self.weapon_empty = Card_display('other', 'empty', True)
        self.weapon_empty.bind(on_press = lambda root:self.show_cards('weapons'))
        container.add_widget(self.weapon_empty)
        if choice_num == 2:
            self.action = 'suspect'
            self.ids['action_image'].source = 'images/Choose_your_Suspect.png'
            self.room_empty = Card_display('room', player.in_room.name, False)
            container.add_widget(self.room_empty)
            for this_card in self.game_reference.cards['rooms']:
                if player.in_room.name == this_card.description:
                    self.select_card(this_card)
        else:
            self.action = 'accuse'
            self.ids['action_image'].source = 'images/Choose_your_Accuse.png'
            self.room_empty = Card_display('other', 'empty', True)
            self.room_empty.bind(on_press = lambda root:self.show_cards('rooms'))
            container.add_widget(self.room_empty)
    
    def show_cards(self, type):
        """Display cards that can be selected of each type

        Callback:
            select_card()

        Args:
            type (str): type of the card (token, weapon, room)
        """
        container = self.ids['cards_to_choose']
        container.clear_widgets()
        for this_card in self.game_reference.cards[type]:
            this_btn = Card_display(this_card.category, this_card.description, True)
            btn_callback = lambda root, temp_card = this_card:self.select_card(temp_card)
            this_btn.bind(on_press = btn_callback)
            container.add_widget(this_btn)
    
    def select_card(self, card):
        """Select the card to be included in the submission

        Args:
            card (Card): the card selected
        """
        self.choice[card.category] = card
        if card.category == 'room':
            self.room_empty.background_normal = 'images/rooms/' + card.description + '_Card.png'
        if card.category == 'weapon':
            self.weapon_empty.background_normal = 'images/weapons/' + card.description + '_Card.png'
        if card.category == 'token':
            self.token_empty.background_normal = 'images/tokens/' + card.description + '_Card.png'

    def submit(self):
        """Submit player choice to game body

        Callback:
            Game_body.submit_callback()
        """
        # Logger.info(self.choice)
        if self.choice['room'] and self.choice['weapon'] and self.choice['token']:
            self.manager.get_screen('game_body').submit_callback(self.action, self.choice)

class Under_Construction(Screen):
    """Page: Under construction sign

    """
    pass

class Game_ending(Screen):
    """Page: Game ends

    """
    def load_page(self, status, player):
        """Preparing to display game ending tips

        Args:
            status (str): win or lose
            player (Player): current player in action
        """
        self.status = status
        self.player = player
        end_image = self.ids['end_image']
        if status == 'win':
            end_image.source = 'images/Win_Scr.png'
        if status == 'lose':
            end_image.source = 'images/Lose_Scr.png'

    def ending_back(self):
        """Handler for 'Back' button on game ending screen
        
        Callback:
            Game_body.next_turn()
        """
        if self.status == 'win':
            self.manager.current = 'main_menu'
        if self.status == 'lose':
            self.player.skipped = True
            self.manager.current = 'game_body'
            self.manager.get_screen('game_body').next_turn(self.player)

class CluedoApp(App):
    """Main class and entry for the app

    """
    def build(self):
        """Loads all screens needed to progress the game

        """
        sm = ScreenManager()
        sm.add_widget(Main_menu(name = 'main_menu'))
        sm.add_widget(New_game(name = 'new_game'))
        sm.add_widget(Game_body(name = 'game_body'))
        sm.add_widget(Player_action(name = 'player_action'))
        sm.add_widget(Under_Construction(name = 'under_construction'))
        sm.add_widget(Game_ending(name = 'game_ending'))
        return sm