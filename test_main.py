import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_task():
    response = await client.post("/task", json={"duration": 1})
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    response = await client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

    await asyncio.sleep(1.5)

    response = await client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "done"}