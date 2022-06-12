"""Article tortoise and pydantic models"""
from pydantic import Field
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models import MainModelMixin
from models import PydanticConfig


class Article(MainModelMixin):
    author = fields.ForeignKeyField("models.User", related_name="articles")
    title = fields.TextField()
    body = fields.TextField()

    class Meta:
        table = "article"


__ArticleCreateInSchema = pydantic_model_creator(
    Article, name="ArticleInSchema", include=("title", "body"))
__ArticleUpdateInSchema = pydantic_model_creator(
    Article, name="ArticleUpdateInSchema", include=("id", "title", "body"))
__ArticleOutSchema = pydantic_model_creator(Article)


class ArticleCreateInSchema(__ArticleCreateInSchema):
    class Config(PydanticConfig):
        ...


class ArticleCreateOutSchema(__ArticleOutSchema):
    class Config(PydanticConfig):
        ...


class ArticleUpdateInSchema(__ArticleUpdateInSchema):
    class Config(PydanticConfig):
        ...


class ArticleUpdateOutSchema(__ArticleOutSchema):
    class Config(PydanticConfig):
        ...


class ArticleOutSchema(__ArticleOutSchema):
    author__login: str = Field(..., alias="author")

    class Config(PydanticConfig):
        ...
