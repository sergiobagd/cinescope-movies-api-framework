import datetime

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

def transfer_money(session, from_account, to_account, amount):
    # Example of func of transaction
    # Let's imagine it's written on the side of tested service
    # And calling method "transfer_money" we like do request in api_manager.movies_api.transfer_money
    """
    Transfers money from one account to other
    :param session: Session SQLAlchemy
    :param from_account: ID of account where we take away money from
    :param to_account: ID of account where we add money to
    :param amount: Sum of transaction money
    """
    # Get accounts
    from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
    to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

    # Check that account has enough money
    if from_account.balance < amount:
        raise ValueError("Not enough money on account")

    # Making transaction
    from_account.balance -= amount
    to_account.balance += amount

    # Save changes in DB
    session.commit()

def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")

def test_accounts_success_transaction_template(db_session):
    # Create new data in DB
    stan = AccountTransactionTemplate(user="Stan_Test10", balance=1000)
    bob = AccountTransactionTemplate(user="Bob_Test15", balance=500)

    # Add new data (users) into session
    db_session.add_all([stan, bob])

    # Commit our changes in DB
    db_session.commit()

    assert stan.balance == 1000
    assert bob.balance == 500

    try:
        # Make transaction 200 rubles from Stan to Bob
        transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

        # Check that balances have changed
        assert stan.balance == 800
        assert bob.balance == 700
    except Exception as e:
        # If error occured, - rollback transaction
        db_session.rollback() # undo all our changes
        pytest.fail(f"Error while sending money: {e}")
    finally:
        # Delete data for testing drom DB
        db_session.delete(stan)
        db_session.delete(bob)
        # Commit our changed in DB
        db_session.commit()

# def test_accounts_fail_transaction_template(db_session):
#     # Create new data in DB
#     stan = AccountTransactionTemplate(user="Stan_Test10", balance=150)
#     bob = AccountTransactionTemplate(user="Bob_Test15", balance=500)
#
#     # Add new data (users) into session
#     db_session.add_all([stan, bob])
#
#     # Commit our changes in DB
#     db_session.commit()
#
#     assert stan.balance == 150
#     assert bob.balance == 500
#
#     try:
#         # Make transaction 200 rubles from Stan to Bob
#         transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)
#
#         # Check that balances have not changed
#         assert stan.balance == 150
#         assert bob.balance == 500
#     except Exception as e:
#         # If error occured, - rollback transaction
#         db_session.rollback() # undo all our changes
#         pytest.fail(f"Error while sending money: {e}")
#     finally:
#         # Delete data for testing drom DB
#         db_session.delete(stan)
#         db_session.delete(bob)
#         # Commit our changed in DB
#         db_session.commit()

def test_delete_movie(super_admin, db_helper):
    """Test for movie deletion"""

    movie_id = 56

    if_movie_exists = db_helper.get_movie_by_id(f"{movie_id}")

    if if_movie_exists is not None:
        delete_response = super_admin.api.movies_api.delete_movie(movie_id)
        get_response = super_admin.api.movies_api.get_specific_movie(movie_id, expected_status=404)
        assert db_helper.get_movie_by_id(f"{movie_id}") is None
    else:
        add_movie_to_db(movie_id, db_helper)
        assert db_helper.get_movie_by_id(f"{movie_id}") is not None
        delete_response = super_admin.api.movies_api.delete_movie(movie_id)
        get_response = super_admin.api.movies_api.get_specific_movie(movie_id, expected_status=404)
        assert db_helper.get_movie_by_id(f"{movie_id}") is None

