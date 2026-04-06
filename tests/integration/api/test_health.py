from httpx import AsyncClient


async def test_health_check_returns_200(client: AsyncClient):
    """
    GIVEN the API server is running
    WHEN requesting GET /api/health
    THEN it should return 200 with status OK
    """
    # Act
    response = await client.get('/api/health')

    # Assert
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}
