import pytest

from constants.models import RegisterUserResponse


class TestUser:
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = response.json()
        created_user_response = RegisterUserResponse(**response_data)
        assert created_user_response.id and created_user_response.id != '', "ID should be not empty"
        assert created_user_response.email == creation_user_data.email
        assert created_user_response.fullName == creation_user_data.fullName
        assert created_user_response.roles == creation_user_data.roles
        assert created_user_response.verified is True

    @pytest.mark.slow
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = response.json()
        created_user_response = RegisterUserResponse(**response_data)
        response_get_by_id = super_admin.api.user_api.get_user_info(created_user_response.id).json()
        response_get_by_email = super_admin.api.user_api.get_user_info(created_user_response.email).json()

        assert response_get_by_id == response_get_by_email, "Response body should be identical"
        assert created_user_response.id and created_user_response.id != '', "ID should be not empty"
        assert created_user_response.email == creation_user_data.email
        assert created_user_response.fullName == creation_user_data.fullName
        assert created_user_response.roles == creation_user_data.roles
        assert created_user_response.verified is True
        assert created_user_response.banned is False

    def test_try_get_user_by_locator_by_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)