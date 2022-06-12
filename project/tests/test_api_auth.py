from . import decode_access_token

TEST_CREDENTIALS = {"login": "test_user", "password": "password"}


def test_sign_up_sign_in(test_app_with_db):
    response = test_app_with_db.post("/auth/sign-up", json=TEST_CREDENTIALS)
    assert response.status_code == 201
    login, user_id = decode_access_token(response.json()["accessToken"])
    assert login == TEST_CREDENTIALS["login"]
    response = test_app_with_db.post("/auth/sign-in", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    login, user_id = decode_access_token(response.json()["accessToken"])
    assert login == TEST_CREDENTIALS["login"]
