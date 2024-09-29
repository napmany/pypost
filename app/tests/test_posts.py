import httpx
import pytest

@pytest.mark.asyncio
async def test_get_posts(async_client: httpx.AsyncClient):
    response = await async_client.get("/api/posts?status=draft&include=tags,user")
    resp = response.json()
    assert response.status_code == 200
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['status'] == 'draft'
    assert len(resp[0]['tags']) == 1
    assert resp[0]['user']['id'] == 1
    
@pytest.mark.asyncio
async def test_get_posts_no_includes(async_client: httpx.AsyncClient):
    response = await async_client.get("/api/posts?status=draft")
    resp = response.json()
    assert response.status_code == 200
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['status'] == 'draft'
    assert 'tags' not in resp[0]
    assert 'user' not in resp[0]
    
@pytest.mark.asyncio
async def test_get_post(async_client: httpx.AsyncClient):
    response = await async_client.get(f"/api/posts/1?include=tags,user,comments")
    assert response.status_code == 200
    assert response.json()['id'] == 1
    
@pytest.mark.asyncio
async def test_get_post_not_found(async_client: httpx.AsyncClient):
    response = await async_client.get("/api/posts/42?include=tags,user,comments")
    assert response.status_code == 404
