from cluedo_game import CluedoGame
import sys

# game = CluedoGame(int(sys.argv[1]) or 5)

def print_setup():
    game = CluedoGame(6)

    print("GameBoard:")
    print(game.gameboard)
    print("\nRooms:")
    print(game.gameboard.rooms)
    print("\nCards:")
    print(type(game.cards))
    print(game.cards)
    print("\nPlayers:")

    for this_player in game.players:
        print(this_player, this_player.cards_in_hand)

    print(type(game.players))

    print(game.players[2].process_suspect(game.cards))

print_setup()