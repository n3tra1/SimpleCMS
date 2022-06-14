"""Auth router"""
from contextlib import suppress

from fastapi import APIRouter
from fastapi_camelcase import CamelModel
from fastapi.exceptions import HTTPException
from pydantic import Field
from tortoise.exceptions import IntegrityError

import bll.user
import models.user

router = APIRouter()


class AccessToken(CamelModel):
    access_token: str = Field(
        ...,
        description="Standard signed JWT HS256 token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7ImxvZ2lu"
        "IjoiaGVsbG8tamltbXkiLCJ1c2VyX2lkIjoiMTMzN2MwZGUxMzM3YzBkZTEzM"
        "zdjMGRlMTMzN2MwZGUifSwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTY1NTA1NT"
        "A1OSwiaWF0IjoxNjU0OTY4NjU5LCJqdGkiOiI3YjRlYTY5MC0xYzQzLTRiYTQ"
        "tYWJlZi0zODE1NzlhNmE3ZTAifQ.i6ZK1HGFxJA2fVj7p6LpF9NC0OPOrj0i2"
        "8Yhzj5bXfk",
    )


@router.post(
    "/sign-up",
    response_model=AccessToken,
    status_code=201,
    responses={
        201: {"description": "Created"},
        400: {"description": "Login is duplicated"},
    },
    description="Create a new user with username and password",
)
async def sign_up(payload: models.user.CredentialsSchema):
    with suppress(IntegrityError):
        user = await bll.user.make_user(payload.login, payload.password)
        return user.make_access_token()
    raise HTTPException(400, f'Login "{payload.login}" is duplicated')


@router.post(
    "/sign-in",
    response_model=AccessToken,
    status_code=200,
    responses={
        200: {"description": "Success"},
        401: {"description": "Unauthorized"},
    },
    description="Get access_token via username and password",
)
async def sign_in(payload: models.user.CredentialsSchema):
    if user := await bll.user.authentication(payload.login, payload.password):
        return user.make_access_token()
    raise HTTPException(401)
