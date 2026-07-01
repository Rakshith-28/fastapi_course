from app import schemas


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@example.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello@example.com"


def test_create_user_duplicate_email(client, test_user):
    res = client.post("/users/", json={"email": test_user["email"], "password": "whatever"})
    assert res.status_code == 409


def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    assert res.json()["email"] == test_user["email"]


def test_get_user_not_found(client):
    res = client.get("/users/88888")
    assert res.status_code == 404
