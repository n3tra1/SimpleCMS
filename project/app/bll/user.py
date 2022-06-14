"""User business login layer"""
from typing import Optional

import bcrypt

from models.user import User

FAKE_SECRET = "$2b$12$pk.vfGdaZKLAFnM.yRiG/.ml.F9WcUkj6wrL5b6dtFj4W5YAtJrWy"

# I added a small trick for excluding a timing attack
# when an attacker can enumerate user list by authentication func.
# But you have a way to enumerate users by make_user func, so in real life
# we need to think about "email as login", one-time passwords, OAuth2, etc.


async def make_user(login: str, password: str) -> User:
    """Make a new user with login and password"""
    return await User.create(login=login, password=password)


async def authentication(login: str, password: str) -> Optional[User]:
    """Get user via login and password"""
    if user := await User.filter(login=login).first():
        return user if user.check_password(password) else None
    # v--- anti timing attack trick ---v
    bcrypt.checkpw(password.encode(), FAKE_SECRET.encode())
    return None
