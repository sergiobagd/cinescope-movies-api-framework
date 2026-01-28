import json
import requests
import logging
import os
from pydantic import BaseModel
from constants.constants import RED, GREEN, RESET


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(self, method, endpoint, data=None, params=None, expected_status=200, need_logging=True):
        """
        Universal method for sending requests
        :param method: HTTP method (GET, POST, PUT, DELETE, etc.)
        :param endpoint: Endpoint (for example: "/login")
        :param data: Request body (JSON data)
        :param params: Query-params
        :param expected_status: Expected status-code
        :param need_logging: Flag for logging (Default: True)
        :return: Object of response requests.Response
        """
        url = f"{self.base_url}{endpoint}"
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))
        response = self.session.request(method, url, json=data, params=params, headers=self.headers)
        if need_logging:
            self.log_request_and_response(response)
        if response.status_code != expected_status:
            raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")
        return response

    def _update_session_headers(self, **kwargs):
        """
        Updating headers of the session.
        :param session: Object requests.Session from API-class.
        :param kwargs: Additional headers.
        """
        self.headers.update(kwargs) # Updating basic headers
        self.session.headers.update(self.headers) # Updating headers in the current session

    def log_request_and_response(self, response):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(f"\tRESPONSE:"
                                 f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                                 f"\nDATA: {RED}{response_data}{RESET}")
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")

