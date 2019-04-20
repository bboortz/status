import os
import tempfile

import pytest

from app import app
from app.utils import config



@pytest.fixture
def client():
	client = app.test_client()

	yield client
