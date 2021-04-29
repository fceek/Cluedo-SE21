# Kivy imports
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
Config.write()

from kivy.lang import Builder
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.screenmanager import (
    ScreenManager, Screen, FadeTransition
)
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.logger import Logger

# Cluedo cmd imports

from cmd.cluedo_game import CluedoGame

Builder.load_file('main.kv')

# Widget Components

class Grid_button(Button):
    def __init__(self, btn_x, btn_y, **kwargs):
        super().__init__(**kwargs)
        self.btn_x = btn_x
        self.btn_y = btn_y

class Trans_button(Button):
    def __init__(self, btn_x, btn_y, **kwargs):
        super().__init__(**kwargs)
        self.btn_x = btn_x
        self.btn_y = btn_y

class Card_display(BoxLayout, ButtonBehavior):
    image_source = StringProperty('default')
    def __init__(self, card_type, card_name, card_clickable = False, **kwargs):
        super().__init__(**kwargs)
        self.card_type = card_type
        self.card_name = card_name
        self.card_clickable = card_clickable
        self.image_source = 'images/' + card_type + 's/' + card_name + '_Card.png'

# App Components

class Main_menu(Screen):
    pass

class New_game(Screen):
    character_chosen = None
    previous_btn = None
    previous_overlay = None

    def choose_character(self, character):
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
        player_count = self.ids['slider_player_num'].value
        if self.character_chosen:
            self.manager.get_screen('game_body').load_page(player_count, self.character_chosen)
            self.manager.transition = FadeTransition()
            self.manager.current = 'game_body'

class Game_body(Screen):
    
    def load_page(self, player_count, character_chosen):
        self.layer_control = self.ids['layer_control']
        self.game_reference = CluedoGame(player_count, character_chosen)

        size = self.game_reference.setup["setup"]["map"]["size"]
        self.gameboard = self.ids['gameboard']
        self.info_text = self.ids['basic_info']
        self.gameboard.rows = size[1]
        self.gameboard.cols = size[0]
        for row in range(0, size[1]):
            for col in range(0, size[0]):
                gameboard_data = self.game_reference.gameboard.board[row][col]
                if gameboard_data == 0:
                    self.gameboard.add_widget(Grid_button(row, col))
                else:
                    self.gameboard.add_widget(Trans_button(row, col))
                #gameboard.add_widget(Button(text = str(row) + ',' + str(col)))
        self.info_text.text = 'Playing as ' + character_chosen

        # while character_chosen.capitalize() not in self.game_reference.players[self.game_reference.next_player].name:
        #     self.game_reference.next_player += 1

        while self.process_turn(self.game_reference.players[self.game_reference.next_player]):
            pass
        #TODO: Game finished screen
    
    def process_turn(self, player) -> bool:
        move_points = self.game_reference.roll_dice()
        reachable_rooms = []
        while len(reachable_rooms) == 0 :
            reachable_rooms = self.game_reference.gameboard.check_reachable_rooms(player, move_points)
            move_points += 1
        self.display_info(player, move_points, reachable_rooms)

    def display_info(self, player, move_points, reachable_rooms):
        self.layer_control.page = 1
        current_layer = self.ids['player_overlay']
        self.ids['dice_points'].text = '[b]' + str(move_points) + '[/b]'
        hand = self.ids['cards_in_hand']
        for this_card in player.cards_in_hand:
            hand.add_widget(Card_display(this_card.category, this_card.description))
        choose_room = self.ids['rooms_to_go']
        for this_room in reachable_rooms:
            btn_callback = lambda *args:self.to_room_on_press(player, this_room)
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
        self.game_reference.gameboard.move_player_to_room(player, room)
        self.info_text.text = player.name + ' has moved to ' + room.name
        self.layer_control.page = 0

    def pressed(self, the_button):
        pass
        # self.info_text.text = "pressed button @ " + str(the_button.btn_x) + ',' + str(the_button.btn_y)


class Under_Construction(Screen):
    pass

class CluedoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main_menu(name = 'main_menu'))
        sm.add_widget(New_game(name = 'new_game'))
        sm.add_widget(Game_body(name = 'game_body'))
        sm.add_widget(Under_Construction(name = 'under_construction'))
        return sm

if __name__ == '__main__':
    CluedoApp().run()