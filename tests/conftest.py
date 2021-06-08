# Copyright 2020-2021 The MathWorks, Inc.

import os, pytest, shutil
from jupyter_matlab_proxy import settings


def pytest_generate_tests(metafunc):
    os.environ["DEV"] = "true"


def __get_matlab_config_file():
    return settings.get(dev=True)["matlab_config_file"]


def __delete_matlab_config_file():
    os.remove(__get_matlab_config_file())


@pytest.fixture(autouse=True, scope="session")
def pre_test_cleanup():
    """A pytest fixture which deletes matlab_config_file before executing tests.

    If a previous pytest run fails, this file may have an empty Dict which leads
    to the server never starting up matlab.
    """
    try:
        __delete_matlab_config_file()
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup the temp directory once we are finished."""

    def delete_matlab_test_dir():
        # Delete matlab_config_file & its owning directory
        matlab_config_file = __get_matlab_config_file()
        matlab_config_dir = os.path.dirname(matlab_config_file)
        shutil.rmtree(matlab_config_dir)

    request.addfinalizer(delete_matlab_test_dir)
