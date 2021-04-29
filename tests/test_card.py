from tests.conftest import LOGGER
from cluedo.cmd.card import Card

def test_card(capsys):

    card = Card('token', 'Rev Green')

    LOGGER.info("CAPTURED: " + str(card.is_answer))
    assert not card.is_answer

    card.make_answer()
    LOGGER.info("CAPTURED: " + str(card.is_answer))
    assert card.is_answer