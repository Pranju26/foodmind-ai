def register_and_login(client, email="targettest@example.com", password="securepass123"):
    client.post("/auth/register", json={"email": email, "password": password})
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    return login_response.json()["access_token"]


def test_targets_fail_without_profile(client):
    token = register_and_login(client)
    response = client.get("/nutrition/targets", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_targets_fail_with_incomplete_profile(client):
    token = register_and_login(client, email="incomplete@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Only partially fill the profile - missing age, height, etc.
    client.post("/profile", json={"sex": "male", "goal": "maintain"}, headers=headers)

    response = client.get("/nutrition/targets", headers=headers)
    assert response.status_code == 400
    assert "incomplete" in response.json()["detail"].lower()


def test_targets_succeed_with_complete_profile(client):
    token = register_and_login(client, email="complete@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/profile", json={
        "sex": "male",
        "age": 22,
        "height_cm": 175,
        "weight_kg": 70,
        "activity_level": "moderate",
        "dietary_preference": "vegetarian",
        "goal": "muscle_gain"
    }, headers=headers)

    response = client.get("/nutrition/targets", headers=headers)
    assert response.status_code == 200

    data = response.json()
    # Verify the exact math from Step 39
    assert round(data["bmr"], 1) == 1688.8
    assert round(data["calorie_target"], 1) == 2917.6
    assert data["protein_grams"] == 126.0
    assert "disclaimer" in data
