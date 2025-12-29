from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest
from backend.Backend import app, get_db


mock_session = MagicMock()


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def mock_db_session():
    return mock_session


client = TestClient(app)


def test_root(mock_db_session):
    response = client.post("/posts/", json={"airline": "Placedholder",
                                            "flight_number": "PH000",
                                            "departure_city": "Placedholder",
                                            "departure_time": "Placedholder",
                                            "stops": 0,
                                            "arrival_time": "Placedholder",
                                            "arrival_city": "Placedholder",
                                            "travel_class": "Placedholder",
                                            "duration": "Placedholder",
                                            "days_left": 0,
                                            "price": 0})
    assert response.status_code == 201
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


def test_get_all_items(mock_db_session):
    response = client.get("/all_items/")
    assert response.status_code == 200
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


def test_get_item(mock_db_session):
    response = client.get("/posts/1")
    assert response.status_code == 200


def test_delete(mock_db_session):
    response = client.delete("/posts/1")
    assert response.status_code == 200
    mock_db_session.delete.assert_called()
    mock_db_session.commit.assert_called()
