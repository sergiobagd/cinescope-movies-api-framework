import datetime
import allure
from db_models.account_transaction import AccountTransactionTemplate
import pytest
from db_models.movie import MovieDBModel
from utils.data_generator import DataGenerator


def add_movie_to_db(movie_id, db_helper):
    created_test_movie = DataGenerator.generate_movie_data()
    created_test_movie["id"] = movie_id
    movie = MovieDBModel(**created_test_movie)
    db_helper.db_session.add(movie)
    db_helper.db_session.commit()

def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")

@allure.epic("Testing transactions")
@allure.feature("Testing transactions between accounts")
class TestAccountTransactionTemplate:
    @allure.story("Validity of money transfer between two accounts")
    @allure.description("""
    This test checks validity of money transfer between two accounts.
    Steps:
    1. Creating two accounts: Stan and Bob.
    2. Transfer 200 rubles from Stan to Bob.
    3. Check that account's balances have changed
    4. Clean up test data""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Testing money transfer between two accounts")
    def test_accounts_success_transaction_template(self, db_session):
        with allure.step("Creating test data in DB: accounts Stan and Bob"):
            stan = AccountTransactionTemplate(user="Stan_Test10", balance=1000)
            bob = AccountTransactionTemplate(user="Bob_Test15", balance=500)
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Function of money transfer: transfer money")
        @allure.description("""
            Func that executes transaction
            Imitation of calling func on the tested service side
            And calling method "transfer_money" we like do request in api_manager.movies_api.transfer_money 
            """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step("Get accounts"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Check that account has enough money"):
                if from_account.balance < amount:
                    raise ValueError("Not enough money on account")

            with allure.step("Making transaction"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Save changes in DB"):
                session.commit()

        with allure.step("Check initial balances"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Make transaction 200 rubles from Stan to Bob"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            with allure.step("Check that balances have changed"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("If error occured, - rollback transaction"):
                db_session.rollback()

            pytest.fail(f"Error while sending money: {e}")

        finally:
            with allure.step("Delete data for testing drom DB"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()

