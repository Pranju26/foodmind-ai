def test_register_new_user(client):
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email_fails(client):
    client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "securepass123"
    })
    response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "anotherpass456"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_short_password_fails(client):
    response = client.post("/auth/register", json={
        "email": "shortpass@example.com",
        "password": "abc"
    })
    assert response.status_code == 422


def test_register_invalid_email_fails(client):
    response = client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "securepass123"
    })
    assert response.status_code == 422


def test_login_with_correct_credentials(client):
    client.post("/auth/register", json={
        "email": "logintest@example.com",
        "password": "correctpass123"
    })
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "correctpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password_fails(client):
    client.post("/auth/register", json={
        "email": "wrongpasstest@example.com",
        "password": "correctpass123"
    })
    response = client.post("/auth/login", json={
        "email": "wrongpasstest@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user_fails(client):
    response = client.post("/auth/login", json={
        "email": "ghost@example.com",
        "password": "anything123"
    })
    assert response.status_code == 401


def test_protected_route_requires_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_protected_route_works_with_valid_token(client):
    client.post("/auth/register", json={
        "email": "protectedtest@example.com",
        "password": "securepass123"
    })
    login_response = client.post("/auth/login", json={
        "email": "protectedtest@example.com",
        "password": "securepass123"
    })
    token = login_response.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "protectedtest@example.com"
