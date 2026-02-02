def test_user_registration(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "user@test.com",
            "password": "strongpassword",
        },
    )

    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"

def test_user_login(client):
    client.post(
        "/auth/register",
        json={
            "email": "user@test.com",
            "password": "strongpassword",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "user@test.com",
            "password": "strongpassword",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
