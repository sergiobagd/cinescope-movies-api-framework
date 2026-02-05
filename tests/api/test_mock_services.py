import datetime
import pytz
import requests
from pytest_mock import mocker
from unittest.mock import Mock
from constants.constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager
from constants.roles import Roles
from constants.models import RegisterUserResponse, TestUser
from pydantic import BaseModel, Field
from practice.service_what_is_today import what_is_today


# Model pydantic for response of server worldclockapi
class WorldClockResponse(BaseModel):
    id: str = Field(alias="$id")
    currentDateTime: str
    utcOffset: str
    isDayLightSavingsTime: bool
    dayOfTheWeek: str
    timeZoneName: str
    currentFileTime: int
    ordinalDate: str
    serviceResponse: None

    class Config:
        # Allow using aliases while parsing JSON
        allow_population_by_field_name = True

# Model for request to service TodayIsHoliday
class DateTimeRequest(BaseModel):
    currentDateTime: str # Format "2025-02-13T21:43Z"

# Model for response from service TodayIsHoliday
class WhatIsTodayResponse(BaseModel):
    message: str

# Function sending request to service worldclockapi: for getting actual date
def get_worldclockapi_time() -> WorldClockResponse:
    # Executing GET request
    response = requests.get("http://worldclockapi.com/api/json/utc/now") # Request to real service
    # Check status code response
    assert response.status_code == 200, "Remote service is not accessible"
    # Parsing JSON response with Pydantic model
    return WorldClockResponse(**response.json())

class TestTodayIsHolidayServiceAPI:
    def test_worldclockap(self): # check if service worldclockap works
        world_clock_response = get_worldclockapi_time()
        # Print current date and time
        current_date_time = world_clock_response.currentDateTime
        print(f"Current date and time: {current_date_time=}")

        assert current_date_time == datetime.datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Data is not matching"

    def test_what_is_today(self): # check if Fake service what_is_today works
        # Requesting current time from service worldclockap
        world_clock_response = get_worldclockapi_time()
        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today",
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json())

        # Check status of response from tested service
        assert what_is_today_response.status_code == 200, "Remote service is not accessible"
        # Parse JSON response ot tested service with Pydantic model
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        # Validate response of tested service
        assert what_is_today_data.message == "Today there is no holiday in Russia"

    def test_what_is_today_BY_MOCK(self, mocker):
        # Create mock for function get_worldclockap_time
        mocker.patch(
            "test_mock_services.get_worldclockapi_time",
            return_value=Mock(
                currentDateTime="2025-01-01T00:00Z" # Mock date for returning holiday of New Year
            )
        )

        # Execute body of previous test again
        world_clock_response = get_worldclockapi_time() # = 2025-01-01T00:00Z

        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today",
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json())

        # Check status of response of tested service
        assert what_is_today_response.status_code == 200, "Remote service is not avaliable"

        # Parse JSON response of tested service with using pydantic model
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())

        assert what_is_today_data.message == "Новый год", "Should be 'Новый год'!!!"

    # Creating Stub for func get_worldclockapi_time()
    def stub_get_wordclockapi_time(self):
        class StubWorldClockResponse:
            def __init__(self):
                self.currentDateTime = "2025-05-09T00:00Z" # Fixed date for Stub
        return StubWorldClockResponse()

    # Test with using Stub
    def test_what_is_today_BY_STUB(self, monkeypatch):
        # Change real func get_worldclockapi_time on stub
        monkeypatch.setattr("test_mock_services.get_worldclockapi_time", self.stub_get_wordclockapi_time)
        # или же можем просто напрямую взять значение из Stub world_clock_response = stub_get_worldclockap_time()

        # Execute body of previous test again
        world_clock_response = get_worldclockapi_time() # Makes call Stub that returns "2025-05-09T00:00Z"

        # Executing request to the tested service
        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today",
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json())

        assert what_is_today_response.status_code == 200
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "День Победы", "Should be 'День Победы'!!!"

    def run_wiremock_worldclockapi_time(self):
        # Launching WireMock server (if uses standalone, this step can be skipped)
        """
        docker run -it --rm -p 8080:8080 --name wiremock wiremock/wiremock:3.12.0
        """
        wiremock_url = "http://localhost:8080/__admin/mappings"
        mapping = {
            "request": {
                "method": "GET",
                "url": "/wire/mock/api/json/utc/now"  # Эмулируем запрос к worldclockapi
            },
            "response": {
                "status": 200,
                "body": '''{
                            "$id": "1",
                            "currentDateTime": "2025-03-08T00:00Z",
                            "utcOffset": "00:00",
                            "isDayLightSavingsTime": false,
                            "dayOfTheWeek": "Wednesday",
                            "timeZoneName": "UTC",
                            "currentFileTime": 1324567890123,
                            "ordinalDate": "2025-1",
                            "serviceResponse": null
                        }'''
            }
        }
        response = requests.post(wiremock_url, json=mapping)
        assert response.status_code == 201, "Couldn't set up wiremock"

    def test_what_is_today_BY_WIREMOCK(self): # This test is like maximum based test
        # Launch our wiremock server
        self.run_wiremock_worldclockapi_time()

        # Making request to WireMock (imitation of worldcloclapi)
        world_clock_response = requests.get("http://localhost:8080/wire/mock/api/json/utc/now")
        assert world_clock_response.status_code == 200, "Remote service is unavailable"
        # Parse JSON response with pydantic model
        current_date_time = WorldClockResponse(**world_clock_response.json()).currentDateTime

        # Send request to tested service what_is_today
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            data=DateTimeRequest(currentDateTime=current_date_time).model_dump_json()
        )

        assert what_is_today_response.status_code == 200, "Remote service is unavailable"
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "Международный женский день", "8 марта же?"

    # Func sending request to fake service worldclockapi to get current date
    def get_fake_worldclockapi_time(self) -> WorldClockResponse:
        # Executing GET request
        response = requests.get("http://127.0.0.1:16001/fake/worldclockapi/api/json/utc/now")
        assert response.status_code == 200, "Remote service is not available"
        return WorldClockResponse(**response.json())

    # Test fake worldclockapi service
    def test_fake_worldclockapi(self): # check if fake service worldclockapi works
        world_clock_response = self.get_fake_worldclockapi_time()
        # Print current date and time
        current_date_time = world_clock_response.currentDateTime
        print(f"Current date and time: {current_date_time=}")

        assert current_date_time == datetime.datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Date isn't matching"

    def test_fake_what_is_today(self): # check if service what_is_today works
        world_clock_response = self.get_fake_worldclockapi_time()

        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today",
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json())

        assert what_is_today_response.status_code == 200, "Remote service is not available"
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "Today there is no holiday in Russia", "There is no holiday!!!"



