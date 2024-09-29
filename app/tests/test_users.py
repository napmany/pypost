import httpx
import pytest
    
@pytest.mark.asyncio
async def test_get_user(async_client: httpx.AsyncClient):
    response = await async_client.get(f"/api/users/1?include=posts,comments")
    resp = response.json()
    assert response.status_code == 200
    assert resp['id'] == 1
    assert resp['name'] == 'tester'
    assert 'posts' in resp
    assert 'comments' in resp
    
@pytest.mark.asyncio
async def test_get_user_no_includes(async_client: httpx.AsyncClient):
    response = await async_client.get(f"/api/users/1")
    resp = response.json()
    assert response.status_code == 200
    assert resp['id'] == 1
    assert resp['name'] == 'tester'
    assert 'posts' not in resp
    assert 'comments' not in resp
    
@pytest.mark.asyncio
async def test_get_user_not_found(async_client: httpx.AsyncClient):
    response = await async_client.get("/api/users/42?include=posts,comments")
    assert response.status_code == 404
