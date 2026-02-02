from app.database import SessionLocal
from app.models import User



def test_protected_route_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_protected_route_authorized(client):
    client.post(
        "/auth/register",
        json={"email": "user@test.com", "password": "pass1234"},
    )

    login = client.post(
        "/auth/login",
        json={"email": "user@test.com", "password": "pass1234"},
    )

    token = login.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"


def test_refresh_token_rotation(client):
    client.post(
        "/auth/register",
        json={"email": "user@test.com", "password": "pass1234"},
    )

    login = client.post(
        "/auth/login",
        json={"email": "user@test.com", "password": "pass1234"},
    )

    refresh_token = login.json()["refresh_token"]

    refresh_1 = client.post(
        "/auth/refresh",
        params={"token": refresh_token},
    )

    assert refresh_1.status_code == 200

    # reuse old refresh token → should fail
    refresh_2 = client.post(
        "/auth/refresh",
        params={"token": refresh_token},
    )

    assert refresh_2.status_code == 401


def test_admin_route_forbidden(client):
    client.post(
        "/auth/register",
        json={"email": "user@test.com", "password": "pass1234"},
    )

    login = client.post(
        "/auth/login",
        json={"email": "user@test.com", "password": "pass1234"},
    )

    token = login.json()["access_token"]

    response = client.get(
        "/admin/stats",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
