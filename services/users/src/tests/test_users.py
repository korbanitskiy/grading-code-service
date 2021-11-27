





def test_user_ping(client):
    response = client.get("/users/ping")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "pong"}


def test_user_add(client):
    response = client.post(
        "/users",
        json={
            'name': "TestUser",
            'email': "test_user@mail.com",
            'is_active': False,
        }
    )
    data = response.json()
    assert response.status_code == 201, response.text
    assert data['message'] == 'TestUser was added'


def test_duplicate_email_error(client):
    user = {'name': "TestUser", 'email': "test_user_error@mail.com", 'is_active': False}
    response_1 = client.post("/users", json=user)
    response_2 = client.post("/users", json=user)
    assert response_1.status_code == 201
    assert response_2.status_code == 400


def test_user_found(client, john):
    response = client.get(f"/users/{john.id}")
    user = response.json()
    assert response.status_code == 200
    assert user['id'] == john.id
    assert user['email'] == john.email
    assert user['is_active'] == john.is_active


def test_user_not_found(client):
    response = client.get(f"/users/{123456789}")
    msg = response.json()
    assert response.status_code == 404
    assert msg == f"User {123456789} is not found"
