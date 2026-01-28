from clients.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api # Here we'll attach object of API Manager for requests

    @property
    def creds(self):
        """Returns cortege (email, password)"""
        return self.email, self.password