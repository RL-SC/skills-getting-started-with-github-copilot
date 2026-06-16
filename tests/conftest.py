import copy
import pytest
from src import app as app_module

# Capture original activities snapshot to restore between tests
_original_activities = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Restore a deep copy of the original activities before each test
    app_module.activities = copy.deepcopy(_original_activities)
    yield
    # No teardown needed; fixture scope ensures isolation
