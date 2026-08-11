def test_root_returns_greeting(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_health_check_reports_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "pass"
