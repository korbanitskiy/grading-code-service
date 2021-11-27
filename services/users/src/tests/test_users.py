def test_user_ping(client):
    response = client.get("/user/ping")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "pong"}


def test_user_add(client, john, db):
    db.delete(john)
    db.commit()
    response = client.post(
        "/user",
        json=john._fields
    )
    data = response.json()
    assert response.status_code == 201, response.text
    assert data['message'] == 'john was added'


def test_duplicate_email_error(client, mary):
    response = client.post("/user", json=mary._fields)
    assert response.status_code == 400


def test_user_found(client, john):
    response = client.get(f"/user/{john.id}")
    user = response.json()
    assert response.status_code == 200
    assert user['id'] == john.id
    assert user['email'] == john.email
    assert user['is_active'] == john.is_active


def test_user_not_found(client):
    response = client.get(f"/user/{123456789}")
    msg = response.json()
    assert response.status_code == 404
    assert msg == f"User {123456789} is not found"


def test_get_all_users(client, john, mary):
    response = client.get("/user/all")
    users = response.json()
    assert response.status_code == 200
    assert users == [
        john._db_fields,
        mary._db_fields,
    ]
