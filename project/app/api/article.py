"""Article router"""
import os
import re
import uuid
from types import MappingProxyType
from typing import List, Optional

from fastapi import APIRouter, Query, Security
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi_jwt import JwtAuthorizationCredentials
from humps import decamelize

import bll.article
import models.article
from api import access_security

SORT_FIELDS_PATTERN = r"-?[a-zA-Z_]+"
SORT_FIELDS_PATTERN_COMPILED = re.compile(SORT_FIELDS_PATTERN)
SORT_FIELDS_REPLACES = MappingProxyType(
    {
        "author": "author__login",
    }
)

router = APIRouter()


@router.post(
    "",
    status_code=201,
    response_model=models.article.ArticleCreateOutSchema,
    responses={
        201: {"description": "Created"},
        401: {"description": "Unauthorized"},
    },
    description="Create an article",
)
async def create_article(
    payload: models.article.ArticleCreateInSchema,
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await bll.article.make(
        credentials["user_id"], payload.title, payload.body
    )


@router.patch(
    "",
    status_code=200,
    response_model=models.article.ArticleUpdateOutSchema,
    responses={
        200: {"description": "Success"},
        400: {"description": "Article is not found"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    description="Update this article",
)
async def update_article(
    payload: models.article.ArticleUpdateInSchema,
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    if article := await bll.article.update(
        credentials["user_id"], payload.id, payload.title, payload.body
    ):
        return article
    raise HTTPException(403)


@router.get(
    "",
    status_code=200,
    response_model=List[models.article.ArticleOutSchema],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad request"},
    },
    description="Get articles",
)
async def get_articles(
    sort_fields: Optional[str] = Query(
        default="createdAt",
        regex=SORT_FIELDS_PATTERN,
        example="author,-createdAt",
        description="Standard multiple order_by command with ASC "
        "and DESC ordering. Default ordering is ASC, "
        'use "-" symbol before *field_name* '
        "if you want to change ordering to DESC. "
        "You can use all fields from the response model",
    ),
    author: Optional[str] = Query(
        default=None,
        example="Author1",
        description="filter by author login",
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=os.getenv("ARTICLE_PAGINATION_LIMIT", 500),
        description="Basic pagination limit",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Basic pagination offset",
    ),
):
    def sort_fields_checker(
        sort_fields_: Optional[str],
    ) -> Optional[List[str]]:
        sort_ = {}
        for s in re.findall(r"-?[a-zA-Z_]+", sort_fields_ or ""):
            field_name = decamelize(s).replace("-", "")
            desc = s[0] == "-"
            sort_[SORT_FIELDS_REPLACES.get(field_name, field_name)] = desc
        if set(models.article.ArticleOutSchema.__fields__).issuperset(sort_):
            return [f"{'-' if v else ''}{k}" for k, v in sort_.items()]

    sort_fields_checked = sort_fields_checker(sort_fields)
    if sort_fields_checked is not None:
        return await bll.article.get(
            sort_fields_checked, author, limit, offset
        )
    raise HTTPException(400, f"Bad request. Check {sort_fields=}")


@router.get(
    "/{article_id}",
    status_code=200,
    response_model=models.article.ArticleOutSchema,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found"},
    },
    description="Get article via article_id",
)
async def get_article_by_id(
    article_id: uuid.UUID = Query(
        description="Article ID",
    )
):
    if article := await bll.article.get(article_id=article_id):
        return article[0]
    raise HTTPException(404, f"Not found an article with {article_id=}")


@router.delete(
    "",
    status_code=204,
    responses={
        204: {"description": "No content"},
        403: {"description": "Forbidden"},
    },
    description="Remove this article from database",
)
async def delete_article(
    article_id: uuid.UUID,
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    if await bll.article.delete(credentials["user_id"], article_id):
        return Response(status_code=204)
    raise HTTPException(403)
