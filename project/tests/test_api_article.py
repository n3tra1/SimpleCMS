import uuid
import datetime

from . import make_auth_header

TEST_CREDENTIALS = {"login": "test_user", "password": "password"}
TEST_ARTICLE = {"title": "test_🕶", "body": "text 👽 " * 1_000_000}


def test_create_article(test_app_with_db):
    response = test_app_with_db.post("/auth/sign-up", json=TEST_CREDENTIALS)
    assert response.status_code == 201
    headers = make_auth_header(response.json()["accessToken"])
    response = test_app_with_db.post(
        "/article", json=TEST_ARTICLE, headers=headers
    )
    assert response.status_code == 201
    r = response.json()
    assert uuid.UUID(r["id"])
    assert r["body"] == TEST_ARTICLE["body"]
    assert r["title"] == TEST_ARTICLE["title"]
    assert r["createdAt"]
    assert r["modifiedAt"]
    response = test_app_with_db.post("/article", json=TEST_ARTICLE)
    assert response.status_code == 401


def test_update_article(test_app_with_db):
    response = test_app_with_db.post("/auth/sign-in", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    headers = make_auth_header(response.json()["accessToken"])
    response = test_app_with_db.post(
        "/article", json=TEST_ARTICLE, headers=headers
    )
    assert response.status_code == 201
    article_id = response.json()["id"]
    created_at = response.json()["createdAt"]
    modified_at = datetime.datetime.fromisoformat(
        response.json()["modifiedAt"]
    )
    response = test_app_with_db.patch(
        "/article",
        headers=headers,
        json={"id": article_id, "title": "1", "body": "2"},
    )
    r = response.json()
    assert r["id"] == article_id
    assert r["title"] == "1"
    assert r["body"] == "2"
    assert r["createdAt"] == created_at
    assert datetime.datetime.fromisoformat(r["modifiedAt"]) > modified_at


def test_delete_article(test_app_with_db):
    response = test_app_with_db.post("/auth/sign-in", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    headers = make_auth_header(response.json()["accessToken"])
    response = test_app_with_db.post(
        "/article", json=TEST_ARTICLE, headers=headers
    )
    assert response.status_code == 201
    article_id = response.json()["id"]
    response = test_app_with_db.delete(
        "/article", headers=headers, params={"article_id": article_id}
    )
    assert response.status_code == 204
    response = test_app_with_db.delete(
        "/article", headers=headers, params={"article_id": article_id}
    )
    assert response.status_code == 403


def test_simple_get(test_app_with_db):
    response = test_app_with_db.post("/auth/sign-in", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    headers = make_auth_header(response.json()["accessToken"])
    response = test_app_with_db.post(
        "/article", json=TEST_ARTICLE, headers=headers
    )
    assert response.status_code == 201
    article_id = response.json()["id"]
    response = test_app_with_db.get(f"/article/{article_id}")
    assert response.status_code == 200
    r = response.json()
    assert uuid.UUID(r["id"])
    assert r["body"] == TEST_ARTICLE["body"]
    assert r["title"] == TEST_ARTICLE["title"]
    assert r["createdAt"]
    assert r["modifiedAt"]


def test_get(test_app_with_db):
    response = test_app_with_db.post("/auth/sign-in", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    headers = make_auth_header(response.json()["accessToken"])

    response = test_app_with_db.post(
        "/article", json=TEST_ARTICLE, headers=headers
    )
    assert response.status_code == 201
    first_article_id = response.json()["id"]

    response = test_app_with_db.post(
        "/article", json=TEST_ARTICLE, headers=headers
    )
    assert response.status_code == 201
    second_article_id = response.json()["id"]

    response = test_app_with_db.get(
        "/article", params={"sort_fields": "-createdAt"}
    )
    assert response.status_code == 200
    r = response.json()
    assert r[0]["id"] == second_article_id
    assert r[1]["id"] == first_article_id
