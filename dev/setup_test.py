from cluedo_game import CluedoGame

# game = CluedoGame(int(sys.argv[1]) or 5)

def print_setup():
    game = CluedoGame(2)

    # print("GameBoard:")
    # print(game.gameboard)
    # print("\nRooms:")
    # print(game.gameboard.rooms)
    #print("\nCards:")
    #print(type(game.cards))
    #print(game.cards)
    # print("\nPlayers:")

    # for this_player in game.players:
    #     print(this_player, this_player.cards_in_hand)

    # print(type(game.players))
    #target_room = game.cards['rooms'][int(input('choose a target room: ')) - 1]
    #print(game.players[2].process_suspect(game.cards,target_room))
    #game.check_suspect(game.players[2].process_suspect(game.cards,game.cards['rooms'][int(input('choose a target room: ')) - 1]),game.players[2])
    #game.gameboard.check_reachable_rooms(game.players[3], 10)
    # print(game.gameboard.check_reachable_rooms(game.gameboard.rooms[2], 0))
    # print(game.gameboard.r3ooms[2])

print_setup()