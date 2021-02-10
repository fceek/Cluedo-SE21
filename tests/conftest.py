from _pytest.fixtures import pytestconfig
import pytest
import logging
import os.path, datetime

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def default_fixture(request):
    filename = os.path.join(
        'logs/pytest/',
        f"{datetime.datetime.now().strftime('%m%d_%H%M%S')}.ptlog"
    )
    request.config.pluginmanager.get_plugin("logging-plugin").set_log_path(filename)
    LOGGER.debug("Test Start")
    yield
    LOGGER.debug("Test End")