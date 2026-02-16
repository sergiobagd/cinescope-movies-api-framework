import datetime
import random
import string
from faker import Faker
from uuid import uuid4
from constants.roles import Roles
faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_user_data() -> dict:
        """Generates data for test user"""

        return {
            "id": f"{uuid4()}", # Generate UUID as string
            "email": DataGenerator.generate_random_email(),
            "full_name": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "verified": False,
            "banned": False,
            "roles": f"{{{Roles.USER.value}}}"
        }

    @staticmethod
    def generate_movie_data() -> dict:
        """Generates data for test user"""

        return {
            "id": faker.random_int(min=1, max=50000),
            "name": DataGenerator.generate_random_email(),
            "price": DataGenerator.generate_random_movie_price(),
            "description": DataGenerator.generate_random_movie_description(),
            "image_url": DataGenerator.generate_random_movie_image_url(),
            "location": DataGenerator.generate_random_movie_location(),
            "published": True,
            "rating": faker.random_int(min=1, max=5),
            "genre_id": DataGenerator.generate_random_movie_genre_id(),
            "created_at": datetime.datetime.now(),
        }

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"breakingbad{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Generation of the password that follows the next rules:
            - 1 letter minimum
            - 1 number minimum
            - Allowed symbols
            - Length is from 8 to 20 symbols
        """

        # Guarantee presence of at least 1 letter and 1 number
        letters = random.choice(string.ascii_letters) # 1 letter
        digits = random.choice(string.digits) # 1 number

        # Addition to the password of random allowed symbols
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18) # Remaining length of the password
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Mixing the password for randomization
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie_name():
        return f"{faker.sentence(nb_words=8)}"

    @staticmethod
    def generate_random_movie_description():
        return f"{faker.sentence(nb_words=15)}"

    @staticmethod
    def generate_random_movie_image_url():
        return f"{faker.url()}"

    @staticmethod
    def generate_random_movie_price():
        return faker.random_int(min=100, max=5000)

    @staticmethod
    def generate_random_movie_location():
        cities_list = ['MSK', 'SPB']
        return f"{faker.random_element(cities_list)}"

    @staticmethod
    def generate_random_movie_genre_id():
        return faker.random_int(min=1, max=10)
