from .cluedo_game import CluedoGame
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
