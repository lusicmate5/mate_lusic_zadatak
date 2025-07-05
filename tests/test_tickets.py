import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.main import app
import pytest_asyncio

@pytest_asyncio.fixture
async def client():
    transport=ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_tickets_returns_list(client):
    response = await client.get("/tickets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]
    assert "status" in data[0]
    assert "priority" in data[0]
    assert "assignee" in data[0]

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_details(client):
    response = await client.get("/tickets/1")
    assert response.status_code == 200
    data = response.json()
    assert "ticket" in data
    assert "raw" in data
    assert "id" in data["ticket"]
    assert "title" in data["ticket"]

@pytest.mark.asyncio
async def test_filter_by_status(client):
    response = await client.get("/tickets?status=open")
    assert response.status_code == 200
    for ticket in response.json():
        assert ticket["status"] == "open"

@pytest.mark.asyncio
async def test_filter_by_priority(client):
    response = await client.get("/tickets?priority=high")
    assert response.status_code == 200
    for ticket in response.json():
        assert ticket["priority"] == "high"

@pytest.mark.asyncio
async def test_search_query(client):
    response = await client.get("/tickets?q=something")
    assert response.status_code == 200
    for ticket in response.json():
        assert "something" in ticket["title"].lower()

import pytest

@pytest.mark.asyncio
async def test_stats_endpoint(client):
    response = await client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "open" in data
    assert "closed" in data
