import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.database import Base, engine


@pytest.fixture(scope="function")
def client():
    # fresh DB for every test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c
