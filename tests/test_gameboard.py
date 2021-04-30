from tests.conftest import LOGGER
from cluedo.cmd.cluedo_game import CluedoGame
from cluedo.cmd.gameboard import GameBoard

def test_gameboard(capsys):

    clue = CluedoGame(2, 'green')
    board = clue.gameboard

    test_start = clue.players[0]
    test_move_points = 11
    clue_rooms = board.check_reachable_rooms(test_start, test_move_points)
    LOGGER.info("CAPTURED: " + str(clue_rooms))

    assert_room1 = 'Ball Room'
    LOGGER.info("ASSUMED: " + str(assert_room1))
    assert_room2 = 'Conservatory'
    LOGGER.info("ASSUMED: " + str(assert_room2))

    assert assert_room1 in str(clue_rooms)
    assert assert_room2 in str(clue_rooms)

    board.move_player_to_room(test_start, clue_rooms[1])
    test_in_room = test_start.in_room
    LOGGER.info("CAPTURED:: " + str(test_in_room))
    assert_in_room = clue_rooms[1]
    LOGGER.info("ASSUMED: " + str(assert_in_room))

    assert test_in_room == assert_in_room

    clue_rooms = board.check_reachable_rooms(test_start, test_move_points)
    LOGGER.info("CAPTURED: " + str(clue_rooms))

    assert_room3 = 'Billiard Room'
    LOGGER.info("ASSUMED: " + str(assert_room3))
    assert_room4 = 'Lounge'
    LOGGER.info("ASSUMED: " + str(assert_room4))

    assert assert_room3 in str(clue_rooms)
    assert assert_room4 in str(clue_rooms)
