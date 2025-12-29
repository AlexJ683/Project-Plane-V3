import pytest
import pandas as pd
# from streamlit.testing.v1 import AppTest
from unittest.mock import patch, MagicMock


from frontend.Frontend import Data_processing


@pytest.fixture
def fake_api_data():
    return [
        {"id": 1, "airline": "TestAir", "flight_number": "TA123",
         "departure_city": "London",
         "departure_time": "Morning",
         "stops": 0,
         "arrival_time": "afternoon",
         "arrival_city": "Rome",
         "travel_class": "economy",
         "duration": "4:00",
         "days_left": 0,
         "price": 42},
        {"id": 2, "airline": "MockJet", "flight_number": "MJ456",
         "departure_city": "Paris",
         "departure_time": "evening",
         "stops": 1,
         "arrival_time": "lunch",
         "arrival_city": "LA",
         "travel_class": "economy+",
         "duration": "12:00",
         "days_left": 0,
         "price": 500},
    ]


@pytest.fixture
def fake_pandas_data(fake_api_data):
    return pd.DataFrame({"id": 1, "airline": "TestAir",
                         "flight_number": "TA123",
                         "departure_city": "London",
                         "departure_time": "Morning",
                         "stops": 0,
                         "arrival_time": "afternoon",
                         "arrival_city": "Rome",
                         "travel_class": "economy",
                         "duration": "4:00",
                         "days_left": 0,
                         "price": 42},
                        {"id": 2, "airline": "MockJet",
                         "flight_number": "MJ456",
                         "departure_city": "Paris",
                         "departure_time": "evening",
                         "stops": 1,
                         "arrival_time": "lunch",
                         "arrival_city": "LA",
                         "travel_class": "economy+",
                         "duration": "12:00",
                         "days_left": 0,
                         "price": 500},)


@pytest.fixture
def mock_requests_get(fake_api_data):
    mock_response = MagicMock()
    mock_response.json.return_value = fake_api_data
    with patch("frontend.Frontend.requests.get", return_value=mock_response):
        yield


@pytest.fixture
def data_processing(mock_requests_get, fake_api_data):
    "creates a fresh instance of the class before every time"
    return Data_processing()


@pytest.fixture
def test_dataframe(fake_api_data):
    return pd.DataFrame(fake_api_data)


class DummyLocation:
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon


"""unit tests"""


# 1
@pytest.mark.unit
def test_load_data(data_processing, mock_requests_get, fake_api_data):
    df = data_processing.load_data()
    assert isinstance(df, pd.DataFrame)


# 2
@pytest.mark.unit
def test_get_column_types(data_processing, mock_requests_get,
                          fake_pandas_data):
    assert data_processing.get_column_types(
        fake_pandas_data) == {"id": int,
                              "airline": str,
                              "flight_number": str,
                              "departure_city": str,
                              "departure_time": str,
                              "stops": int,
                              "arrival_time": str,
                              "arrival_city": str,
                              "travel_class": str,
                              "duration": str,
                              "days_left": int,
                              "price": int}


# 3
@pytest.mark.unit
def test_check_data(data_processing, mock_requests_get, fake_pandas_data):
    mock_response = {"id": int, "airline": str, "flight_number": str,
                     "departure_city": str,
                     "departure_time": str,
                     "stops": int,
                     "arrival_time": str,
                     "arrival_city": str,
                     "travel_class": str,
                     "duration": str,
                     "days_left": int,
                     "price": int}
    weird_data = pd.DataFrame({"id": 1, "airline": "TestAir",
                               "flight_number": "TA123",
                               "departure_city": "London",
                               "departure_time": 4,
                               "stops": 0,
                               "arrival_time": "afternoon",
                               "arrival_city": "Rome",
                               "travel_class": "economy",
                               "duration": "4:00",
                               "days_left": 0,
                               "price": 42},
                              {"id": 2, "airline": "MockJet",
                               "flight_number": "MJ456",
                               "departure_city": "Paris",
                               "departure_time": 5,
                               "stops": 1,
                               "arrival_time": "lunch",
                               "arrival_city": "LA",
                               "travel_class": "economy+",
                               "duration": "12:00",
                               "days_left": 0,
                               "price": 500},)

    with patch("frontend.Frontend.Data_processing.get_column_types",
               return_value=mock_response):
        assert data_processing.check_data(fake_pandas_data) == "Data is valid"
        assert data_processing.check_data(fake_pandas_data.drop
                                          (columns=["airline"])) == "Missing "
        "column: airline"
        assert data_processing.check_data(weird_data) == "Incorrect data type"
        " in column: departure_time. Expected str."


# 4
@pytest.mark.unit
def test_convert_to_JSON(data_processing, mock_requests_get,
                         fake_pandas_data, fake_api_data):
    assert data_processing.convert_to_JSON(
        fake_pandas_data) == fake_pandas_data.to_dict(orient="records")


# 5
@pytest.mark.unit
def test_post_data(data_processing,
                   mock_requests_get, fake_pandas_data):
    assert data_processing.post_data() == "Data posted successfully"
    data_processing.data_for_upload = {"test": "test"}
    assert data_processing.post_data() == "Data type invalid, data not posted"


# 6
@pytest.mark.unit
def test_w2n_stuff(data_processing, mock_requests_get):
    with patch("frontend.Frontend.w2n.word_to_num", return_value=1):
        assert data_processing.w2n_stuff("one") == 1
    with patch("frontend.Frontend.w2n.word_to_num", side_effect=ValueError):
        assert data_processing.w2n_stuff("two_or_more") == 3


# 7
@pytest.mark.unit
def test_geo_data_returns_coordinates(data_processing):

    fake_dep = DummyLocation(51.5074, -0.1278)   # London
    fake_arr = DummyLocation(40.7128, -74.0060)  # New York

    mock_geolocator = MagicMock()
    mock_geolocator.geocode.side_effect = [fake_dep, fake_arr]

    with patch("frontend.Frontend.Data_processing.get_geolocator",
               return_value=mock_geolocator):
        assert data_processing.geo_data("London", "New York") == {
            "latitude_departure": 51.5074,
            "longitude_departure": -0.1278,
            "latitude_arrival": 40.7128,
            "longitude_arrival": -74.0060,
        }


"""integration tests"""


# 8
@pytest.mark.integration
def test_for_check_data_integration(data_processing, mock_requests_get,
                                    fake_pandas_data):
    weird_data = pd.DataFrame({"id": 1, "airline": "TestAir",
                               "flight_number": "TA123",
                               "departure_city": "London",
                               "departure_time": 4,
                               "stops": 0,
                               "arrival_time": "afternoon",
                               "arrival_city": "Rome",
                               "travel_class": "economy",
                               "duration": "4:00",
                               "days_left": 0,
                               "price": 42},
                              {"id": 2, "airline": "MockJet",
                               "flight_number": "MJ456",
                               "departure_city": "Paris",
                               "departure_time": 5,
                               "stops": 1,
                               "arrival_time": "lunch",
                               "arrival_city": "LA",
                               "travel_class": "economy+",
                               "duration": "12:00",
                               "days_left": 0,
                               "price": 500},)
    assert data_processing.check_data(fake_pandas_data) == "Data is valid"
    assert data_processing.check_data(fake_pandas_data.drop(columns=[
        "airline"])) == "Missing column: airline"
    assert data_processing.check_data(weird_data) == "Incorrect data type"
    " in column: departure_time. Expected str."


# 9
@pytest.mark.integration
def test_w2n_integration(data_processing, mock_requests_get):
    assert data_processing.w2n_stuff("one") == 1
    assert data_processing.w2n_stuff("two_or_more") == 3


# 10
@pytest.mark.integration
def test_geo_data_intdegration(data_processing, mock_requests_get,
                               fake_pandas_data):
    result = data_processing.geo_data("London", "Paris")
    assert result is not None
    assert 48 <= result["latitude_arrival"] <= 49
    assert 51 <= result["latitude_departure"] <= 52


"""@pytest.mark.streamlit_tests
def test_search_page_integration(data_processing, mock_requests_get,
fake_pandas_data):
    app = web_app()

    app.data_processing.data = pd.DataFrame([{
        "flight_number": "TA123",
        "departure_city": "London",
        "arrival_city": "Rome",
        "airline": "TestAir",
        "price": 100,
        "duration": 120,
        "stops": 0,
        "arrival_time": "afternoon",
        "departure_time": "Morning",
        "travel_class": "economy",
        "days_left": 42,
        "id": 0
    }])

   # Run the search_page inside a test session
    session = AppTest.from_function(app.search_page).run()

    # Simulate user typing into the text input
    session.text_input("flight_number_input").set_value("TA123")
    session.run()

    # Assert that "Flight Details:" was rendered
    assert "Flight Details:" in session.get_text()

    # Assert that the dataframe contains the flight number
    df = session.get_dataframe()
    assert "TA123" in df["flight_number"].values
"""
