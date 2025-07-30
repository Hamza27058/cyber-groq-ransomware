import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
        assert r.status_code == 200

@pytest.mark.asyncio
async def test_ask():
    payload = {"query": "Who were the latest 3 victims?", "limit": 3}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/ask", json=payload)
        assert r.status_code == 200
        assert "answer" in r.json()