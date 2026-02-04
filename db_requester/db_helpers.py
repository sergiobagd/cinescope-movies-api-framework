from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movie import MovieDBModel


class DBHelper:
    """
    Class with methods to work with DB
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Creates test user"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def create_test_movie(self, movie_data: dict) -> UserDBModel:
        """Creates test user"""
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie


    def get_user_by_id(self, user_id: str):
        """Gets user by id"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Gets user by email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def get_movie_by_name(self, name: str):
        """Gets movie by name"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def get_movie_by_id(self, id: str):
        """Gets movie by id"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == id).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Checks user existing by email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel):
        """Deletes user"""
        self.db_session.delete(user)
        self.db_session.commit()

    def delete_movie(self, movie: MovieDBModel):
        """Deletes movie"""
        self.db_session.delete(movie)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Cleans up test data"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

