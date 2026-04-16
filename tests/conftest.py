import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app, follow_redirects=False)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore in-memory activities to their original state after each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
