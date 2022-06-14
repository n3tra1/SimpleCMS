import bcrypt
import bll.user
import models.user

TEST_CREDENTIALS = {"login": "test_🕶", "password": "password🕶"}
WRONG_LOGIN = "wrong_login"
WRONG_PASSWORD = "wrong_password"


async def test_make_user():
    user = await bll.user.make_user(
        TEST_CREDENTIALS["login"], TEST_CREDENTIALS["password"]
    )
    assert isinstance(user, models.user.User)
    assert user.login == TEST_CREDENTIALS["login"]
    db_user = await bll.user.User.filter(id=user.id).first()
    assert user == db_user
    assert (
        bcrypt.checkpw(
            TEST_CREDENTIALS["password"].encode(), db_user.secret.encode()
        )
        is True
    )


async def test_authentication():
    user = await bll.user.authentication(
        TEST_CREDENTIALS["login"], TEST_CREDENTIALS["password"]
    )
    assert isinstance(user, bll.user.User)
    assert user.login == TEST_CREDENTIALS["login"]

    none_user = await bll.user.authentication(
        TEST_CREDENTIALS["login"], WRONG_PASSWORD
    )
    assert none_user is None

    none_user = await bll.user.authentication(WRONG_LOGIN, WRONG_PASSWORD)
    assert none_user is None
