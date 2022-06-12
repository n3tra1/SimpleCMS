import base64
import json
import uuid
from typing import Tuple


def decode_access_token(access_token: str) -> Tuple[str, uuid.UUID]:
    _, body, _ = access_token.split('.')
    jwt = json.loads(base64.b64decode(body + ('=' * (-len(body) % 4))))
    return jwt["subject"]["login"], uuid.UUID(jwt["subject"]["user_id"])


def make_auth_header(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}
