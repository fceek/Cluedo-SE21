from tests.conftest import LOGGER
from cluedo.cmd.cluedo_game import CluedoGame

def test_cluedo_game(capsys):

    # this is combined with unit test of
    # __init__(), load_setup(), load_cards(), load_players() and deal_card()

    clue = CluedoGame(2, 'green')
    
    clue_type = type(clue)
    LOGGER.info("CAPTURED: " + str(clue_type))
    assert_type = CluedoGame
    LOGGER.info("ASSUMED: " + str(assert_type))
    assert clue_type == assert_type

    clue_player_count = len(clue.players)
    LOGGER.info("CAPTURED: " + str(clue_player_count))
    assert_player_count = 2
    LOGGER.info("ASSUMED: " + str(assert_player_count))
    assert clue_player_count == assert_player_count

    clue_first_player = clue.players[clue.next_player].name
    LOGGER.info("CAPTURED: " + str(clue_first_player))
    assert_first_player = 'Rev Green'
    LOGGER.info("ASSUMED: " + str(assert_first_player))
    assert clue_first_player == assert_first_player

    clue_cards_number = (len(clue.cards['tokens'])
                        + len(clue.cards['weapons'])
                        + len(clue.cards['rooms'])
                        )
    LOGGER.info("CAPTURED: " + str(clue_cards_number))
    assert_cards_number = 21
    LOGGER.info("ASSUMED: " + str(assert_cards_number))
    assert clue_cards_number == assert_cards_number

    clue_cards_dealt = 0
    for this_player in clue.players:
        clue_cards_dealt += len(this_player.cards_in_hand)
    LOGGER.info("CAPTURED: " + str(clue_cards_dealt))
    assert_cards_dealt = 18
    LOGGER.info("ASSUMED: " + str(assert_cards_dealt))
    assert clue_cards_dealt == assert_cards_dealt

def test_load_gameboard(capsys):

    clue = CluedoGame(2, 'green')

    clue_gameboard_plot1 = clue.gameboard.board[0][0]
    LOGGER.info("CAPTURED: " + str(clue_gameboard_plot1))
    assert_gameboard_plot1 = 1
    LOGGER.info("ASSUMED: " + str(assert_gameboard_plot1))
    assert clue_gameboard_plot1 == assert_gameboard_plot1

    clue_gameboard_plot2 = clue.gameboard.board[8][10]
    LOGGER.info("CAPTURED: " + str(clue_gameboard_plot2))
    assert_gameboard_plot2 = 888
    LOGGER.info("ASSUMED: " + str(assert_gameboard_plot2))
    assert clue_gameboard_plot2 == assert_gameboard_plot2

    clue_gameboard_plot3 = clue.gameboard.board[23][15]
    LOGGER.info("CAPTURED: " + str(clue_gameboard_plot3))
    assert_gameboard_plot3 = 0
    LOGGER.info("ASSUMED: " + str(assert_gameboard_plot3))
    assert clue_gameboard_plot3 == assert_gameboard_plot3

def test_generate_answer(capsys):

    clue = CluedoGame(2, 'green')

    clue_answer_count = 0
    clue_answer_count_token = 0
    clue_answer_count_weapon = 0
    clue_answer_count_room = 0
    for this_card in clue.cards['tokens']:
        if this_card.is_answer:
            clue_answer_count += 1
            clue_answer_count_token = 1
    for this_card in clue.cards['weapons']:
        if this_card.is_answer:
            clue_answer_count += 1
            clue_answer_count_weapon = 1
    for this_card in clue.cards['rooms']:
        if this_card.is_answer:
            clue_answer_count += 1
            clue_answer_count_room = 1

    assert_answer_count = 3
    assert_answer_count_token = 1
    assert_answer_count_weapon = 1
    assert_answer_count_room = 1

    LOGGER.info("CAPTURED: " + str(clue_answer_count))
    LOGGER.info("ASSUMED: " + str(assert_answer_count))
    LOGGER.info("CAPTURED: " + str(clue_answer_count_token))
    LOGGER.info("ASSUMED: " + str(assert_answer_count_token))
    LOGGER.info("CAPTURED: " + str(clue_answer_count_weapon))
    LOGGER.info("ASSUMED: " + str(assert_answer_count_weapon))
    LOGGER.info("CAPTURED: " + str(clue_answer_count_room))
    LOGGER.info("ASSUMED: " + str(assert_answer_count_room))

    assert clue_answer_count == assert_answer_count
    assert clue_answer_count_token == assert_answer_count_token
    assert clue_answer_count_weapon == assert_answer_count_weapon
    assert clue_answer_count_room == assert_answer_count_room


def test_roll_dice(capsys):

    clue = CluedoGame(2, 'green')

    for i in range (10):
        clue_dice = clue.roll_dice()
        LOGGER.info("CAPTURED: " + str(clue_dice))
        LOGGER.info("ASSUMED: " + 'Range 2 - 13')
        assert clue_dice > 1 and clue_dice < 13

def test_display_info(capsys):

    clue = CluedoGame(2, 'green')

    test_player = clue.players[0]
    test_move_points = 10
    test_reachable_rooms = []
    clue.display_info(test_player, test_move_points, test_reachable_rooms)
    clue_captured = capsys.readouterr()
    LOGGER.info("CAPTURED: " + str(clue_captured))

    assert_output_part1 = 'Rev Green'
    LOGGER.info("ASSUMED: " + str(assert_output_part1))
    assert_output_part2 = 'you can move 10 steps'
    LOGGER.info("ASSUMED: " + str(assert_output_part2))
    assert_output_part3 = 'you can reach those rooms []'
    LOGGER.info("ASSUMED: " + str(assert_output_part3))

    assert assert_output_part1 in clue_captured.out
    assert assert_output_part2 in clue_captured.out
    assert assert_output_part3 in clue_captured.out

def test_check_accuse(capsys):

    clue = CluedoGame(2, 'green')

    test_answer = {}
    for this_card in clue.cards['tokens']:
        if this_card.is_answer:
            test_answer['token'] = this_card
    for this_card in clue.cards['weapons']:
        if this_card.is_answer:
            test_answer['weapon'] = this_card
    for this_card in clue.cards['rooms']:
        if this_card.is_answer:
            test_answer['room'] = this_card
    
    LOGGER.info("CAPTURED: " + str(test_answer))
    assert clue.check_accuse(test_answer)
