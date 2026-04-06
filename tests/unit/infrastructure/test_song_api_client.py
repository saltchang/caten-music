from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.infrastructure.song_api_client import HttpxSongApiClient


@pytest.fixture
def client():
    return HttpxSongApiClient(base_url='http://test-api:3000')


def _make_response(status_code: int, json_data):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data
    return resp


class TestSearch:
    async def test_search_by_title(self, client):
        """
        GIVEN a mock API that returns one song matching the title
        WHEN searching by title
        THEN the client calls the correct URL and returns one result
        """
        # Arrange
        resp = _make_response(200, [{'sid': '1001001', 'title': 'Test Song'}])
        mock_get = AsyncMock(return_value=resp)

        with patch.object(client._client, 'get', mock_get):
            # Act
            result = await client.search(title='Test')

            # Assert
            mock_get.assert_called_once()
            call_url = mock_get.call_args[0][0]
            assert 'title=Test' in call_url
            assert len(result) == 1

    async def test_search_returns_empty_on_error(self, client):
        """
        GIVEN a mock API that returns a 404 status
        WHEN searching by title
        THEN the client returns an empty list
        """
        # Arrange
        resp = _make_response(404, [])
        mock_get = AsyncMock(return_value=resp)

        with patch.object(client._client, 'get', mock_get):
            # Act
            result = await client.search(title='Nonexistent')

            # Assert
            assert result == []


class TestGetBySid:
    async def test_get_by_sid(self, client):
        """
        GIVEN a mock API that returns a song for a given SID
        WHEN fetching by SID
        THEN the client calls the correct URL and returns one result
        """
        # Arrange
        resp = _make_response(200, [{'sid': '1001001', 'title': 'Song'}])
        mock_get = AsyncMock(return_value=resp)

        with patch.object(client._client, 'get', mock_get):
            # Act
            result = await client.get_by_sid('1001001')

            # Assert
            call_url = mock_get.call_args[0][0]
            assert '/api/songs/sid/1001001' in call_url
            assert len(result) == 1


class TestGetBySids:
    async def test_get_by_sids(self, client):
        """
        GIVEN a mock API that returns songs for multiple SIDs
        WHEN fetching by a list of SIDs
        THEN the client calls the correct URL with joined SIDs and returns all results
        """
        # Arrange
        resp = _make_response(200, [{'sid': '1001001'}, {'sid': '1001002'}])
        mock_get = AsyncMock(return_value=resp)

        with patch.object(client._client, 'get', mock_get):
            # Act
            result = await client.get_by_sids(['1001001', '1001002'])

            # Assert
            call_url = mock_get.call_args[0][0]
            assert '1001001+1001002' in call_url
            assert len(result) == 2


class TestGetRandom:
    async def test_get_random(self, client):
        """
        GIVEN a mock API that returns one random song
        WHEN requesting random songs with a count of 6
        THEN the client calls the correct URL and returns the result
        """
        # Arrange
        resp = _make_response(200, [{'sid': '1001001'}])
        mock_get = AsyncMock(return_value=resp)

        with patch.object(client._client, 'get', mock_get):
            # Act
            result = await client.get_random(6)

            # Assert
            call_url = mock_get.call_args[0][0]
            assert '/api/songs/random/6' in call_url
            assert len(result) == 1
