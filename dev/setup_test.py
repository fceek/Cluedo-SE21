from cluedo_game import CluedoGame
import sys

game = CluedoGame(int(sys.argv[1]) or 5)

def print_setup():
    game = CluedoGame(6)

    print("GameBoard:")
    print(game.gameboard)
    print("\nRooms:")
    print(game.gameboard.rooms)
    print("\nCards:")
    print(game.cards)
    print("\nPlayers:")
    print(game.players)