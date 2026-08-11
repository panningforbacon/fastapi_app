def test_root_returns_greeting(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json().get("message")[:5] == "Hello"


def test_health_check_reports_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json().get("status") == "pass"
