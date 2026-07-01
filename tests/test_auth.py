import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload.get("user_id") == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong@example.com", "password123", 403),
        ("user1@example.com", "wrongpassword", 403),
        ("wrong@example.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("user1@example.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
