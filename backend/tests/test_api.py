import pytest
from httpx import AsyncClient, ASGITransport

from backend.src.main import app

@pytest.mark.asyncio # для тестирования асинхронной api
async def test_ge_hotels():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/hotels_all")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2


@pytest.mark.asyncio # для тестирования асинхронной api
async def test_post_hotels():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/hotels_all", json={
            "owner": "test",
            "title": "test",
        })
        assert response.status_code == 200

        data = response.json()
        assert data == {"status": True, "message": "Отель успешно добавлен"}
