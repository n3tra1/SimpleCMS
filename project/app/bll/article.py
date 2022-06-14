"""Article business logic layer"""
import datetime
import uuid
from typing import Iterable, List, Optional

from models.article import Article


async def make(author_id: uuid.UUID, title: str, body: str) -> Article:
    """Make a new article"""
    return await Article.create(author_id=author_id, title=title, body=body)


async def update(
    author_id: uuid.UUID, article_id: uuid.UUID, title: str, body: str
) -> Optional[Article]:
    """Update an article via article_id"""
    row_count = await Article.filter(
        author_id=author_id, id=article_id
    ).update(title=title, body=body, modified_at=datetime.datetime.utcnow())
    return await Article.filter(id=article_id).first() if row_count else None


async def get(
    sort_fields: Iterable[str] = (),
    author: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    article_id: Optional[uuid.UUID] = None,
) -> List[dict]:
    """
    :param sort_fields: standard order_by
           https://tortoise-orm.readthedocs.io/en/latest/query.html?highlight=order_by#tortoise.queryset.QuerySet.order_by
    :param author: filter by author login
    :param limit: basic SQL LIMIT
    :param offset: basic SQL OFFSET
    :param article_id: if you use this param then other params was ignored
    :return: List of dictionaries
    """
    q = Article.all().prefetch_related("author__login")
    if article_id is None:
        q = q.filter(author__login=author) if author else q
        q = q.order_by(*sort_fields) if sort_fields else q
        q = q.limit(limit) if limit else q
        q = q.offset(offset) if offset else q
    else:
        q = q.filter(id=article_id)
    q = q.values(
        "id", "body", "title", "created_at", "modified_at", "author__login"
    )
    return await q


async def delete(author_id: uuid.UUID, article_id: uuid.UUID) -> bool:
    """Delete an article via article_id"""
    return bool(
        await Article.filter(author_id=author_id, id=article_id).delete()
    )
