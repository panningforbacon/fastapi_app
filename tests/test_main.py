from httpx import AsyncClient


async def test_root_returns_greeting(client: AsyncClient) -> None:
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json().get("message")[:5] == "Hello"


async def test_health_check_reports_ok(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json().get("status") == "pass"
