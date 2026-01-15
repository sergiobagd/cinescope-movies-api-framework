import json
import requests
import logging
import os

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

    def send_request(self, method, endpoint, data=None, expected_status=200, need_logging=True):
        """
        Universal method for sending requests
        :param method: HTTP method (GET, POST, PUT, DELETE, etc.)
        :param endpoint: Endpoint (for example: "/login")
        :param data: Request body (JSON data)
        :param expected_status: Expected status-code
        :param need_logging: Flag for logging (Default: True)
        :return: Object of response requests.Response
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, json=data, headers=self.headers)
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
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.log(logging.INFO, "\n" + "=" * 40 + " REQUEST " + "=" * 40)
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            self.logger.log(logging.INFO, "\n" + "=" * 40 + " RESPONSE " + "=" * 40)
            if not response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response.status_code}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response.status_code}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.log(logging.INFO, "=" * 80 + "\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")
