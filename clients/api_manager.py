from clients.auth_api import AuthAPI
from clients.user_api import UserAPI
from clients.movies_api import MoviesAPI

class ApiManager:
    """
    Class for managing API classes with the same HTTP-session
    """
    def __init__(self, session):
        """
        Initialization of ApiManager
        :param session: HTTP session which is used by all of  API classes
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)

    def close_session(self):
        self.session.close()

