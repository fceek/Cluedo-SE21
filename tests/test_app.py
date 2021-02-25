from tests.conftest import LOGGER
import cluedo

def test_app(capsys):

    cluedo.Cluedo.run()

    captured = capsys.readouterr()
    res = "Hello World"

    LOGGER.info("CAPTURE: " + str(captured))
    LOGGER.info("ASSUMED: " + str(res))

    assert res in captured.out