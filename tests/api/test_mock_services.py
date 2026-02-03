import datetime
import pytz
import requests
from constants.constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager
from constants.roles import Roles
from constants.models import RegisterUserResponse, TestUser
from pydantic import BaseModel, Field


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
        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today", data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime))


        # Check status of response from tested service
        assert what_is_today_response.status_code == 200, "Remote service is not accessible"
        # Parse JSON response ot tested service with Pydantic model
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        # Validate response of tested service
        assert what_is_today_data.message == "Today there is no holiday in Russia"