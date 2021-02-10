from tests.conftest import LOGGER
from cluedo import Cluedo

def test_app(capsys):

    Cluedo.run()

    captured = capsys.readouterr()
    res = "Hello World"

    LOGGER.info("CAPTURE: " + str(captured))
    LOGGER.info("ASSUMED: " + str(res))

    assert res in captured.out