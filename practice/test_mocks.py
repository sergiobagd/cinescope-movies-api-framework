from unittest.mock import Mock
import pytest
import requests

# Pseudocode showing real class which goes to Gismeteo.ru
# And takes actual temperature in celcius
class ThermometerService:
    def get_weather(self, city) -> int:
        return gismeteo_client.request_weather(city)

gismeteo_mock = Mock(spec=ThermometerService)
gismeteo_mock.get_weather.return_value = 100
# mock.some_method,side_effect = [-100, 0, 100] # Sequence calls

# Mock for test isolation
def test_fetch_data():
    # Tested code use our service but give mock data
    temperature = gismeteo_mock.get_weather("Moscow")

    assert my_service.check_temperature(temperature) == -100
    assert my_service.check_temperature(temperature) == 0
    assert my_service.check_temperature(temperature) == 100


# Mock for emulation of rare situations
def test_complex_scenario():
    mock = Mock()
    mock.some_method.side_effect = [None, Exception("Network error")]

    assert mock.some_method() is None # First call
    try:
        mock.some_method() # Second call
    except Exception as e:
        assert str(e) == "Network error"

# Stub
# Stub — это объект, который возвращает заранее определенные данные в ответ
# на вызовы методов (как раз то что мы рассмотрели выше).
# Он используется для замены реального объекта, чтобы тестируемый код мог
# работать с предсказуемыми данными.
class Database:
    def get_user(self, user_id):
        # Real code for getting user from DB
        pass

class StubDatabase:
    def get_user(self, user_id):
        return {"id": user_id, "name": "John Doe"}

# В этом примере StubDatabase— это заглушка, которая всегда возвращает одного и
# того же пользователя, независимо от переданного user_id.
# (Очень похоже на то что было выше)
def test_get_user():
    db = StubDatabase()
    user = db.get_user(1)
    assert user["name"] == "John Doe"

# Mock - это объект, который позволяет проверять, как и с какими аргументами
# вызывались его методы.
# Моки используются для проверки взаимодействия между объектами.

class EmailService:
    def send_email(self, to, subject, body):
        # Real code for sending email
        pass

def test_send_email():
    email_service = Mock()
    email_service.send_email("user@example.com", "Test subject", "Hey buddy!")
    email_service.send_email.assert_called_once_with("user@example.com", "Test subject", "Hey buddy!")


# Setting WireMock for our gismeteo mock
def setup_wiremock_mock():
    url = "http://localhost:8080/__admin/mappings"
    payload = {
        "request": {
            "method": "GET",
            "url": "/gismeteo/get/weather"  # мы указываем что если ктото сделате запрос на ручку
            # http://localhost:8080/gismeteo/get/weather
        },
        "response": {
            "status": 200,  # ему вернется ответ с кодом 200
            "body": '{"temperature": 25}',
            "headers": {
                "Content-Type": "application/json"
            }
        }
    }

    response = requests.post(url, json=payload) # Send request to our WireMock

def test_wiremock():
    setup_wiremock_mock()
    response = requests.get("http://localhost:8080/gismeteo/get/weather")
    assert response.status_code == 200
    assert response.json() == {"temperature": 25}
    print("Test passed!")







