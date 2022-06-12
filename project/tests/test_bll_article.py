import bll.user
import bll.article
import models.article


async def test_make_article():
    user_id = (await bll.user.make_user("test1", "test")).id
    article = await bll.article.make(user_id, "test_title", "test_body")
    assert isinstance(article, models.article.Article)
    assert article.title == "test_title"
    assert article.body == "test_body"
    db_article = await models.article.Article.filter(id=article.id).first()
    assert article == db_article


async def test_update_article():
    user_id = (await bll.user.make_user("test2", "test")).id
    article = await bll.article.make(user_id, "test_title", "test_body")
    await bll.article.update(user_id, article.id, "second_title", "nothing")
    db_article = await models.article.Article.filter(id=article.id).first()
    assert db_article.title == "second_title"
    assert db_article.body == "nothing"
    assert article == db_article


async def test_delete_article():
    user_id = (await bll.user.make_user("test3", "test")).id
    article = await bll.article.make(user_id, "test_title", "test_body")
    await bll.article.delete(user_id, article.id)
    db_article = await models.article.Article.filter(id=article.id).first()
    assert db_article is None


async def test_get_one_article():
    user_id = (await bll.user.make_user("test4", "test")).id
    article = await bll.article.make(user_id, "test_title", "test_body")
    db_article = await bll.article.Article.filter(id=article.id).first()
    assert article == db_article


async def test_get_article():
    user_id = (await bll.user.make_user("test5", "test")).id
    for _ in range(1000):
        await bll.article.make(user_id, "test_title", "test_body")
    assert len(await bll.article.get(limit=500)) == 500
