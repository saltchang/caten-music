from typing import Any

import httpx


class HttpxSongApiClient:
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._client = httpx.AsyncClient(timeout=30.0)

    async def search(
        self,
        title: str = '',
        lyrics: str = '',
        lang: str = '',
        collection: str = '',
        tonality: str = '',
    ) -> list[dict[str, Any]]:
        url = f'{self._base_url}/api/songs/search?lang={lang}&c={collection}&to={tonality}&title={title}&lyrics={lyrics}&test=0'
        response = await self._client.get(url)
        if response.status_code != 200:
            return []
        return response.json()

    async def get_by_sid(self, sid: str) -> list[dict[str, Any]]:
        url = f'{self._base_url}/api/songs/sid/{sid}'
        response = await self._client.get(url)
        if response.status_code != 200:
            return []
        return response.json()

    async def get_by_sids(self, sids: list[str]) -> list[dict[str, Any]]:
        sids_str = '+'.join(sids)
        url = f'{self._base_url}/api/songs/sid/{sids_str}'
        response = await self._client.get(url)
        if response.status_code != 200:
            return []
        return response.json()

    async def get_random(self, amount: int) -> list[dict[str, Any]]:
        url = f'{self._base_url}/api/songs/random/{amount}'
        response = await self._client.get(url)
        if response.status_code != 200:
            return []
        return response.json()

    async def create_song(self, data: dict[str, Any]) -> str:
        url = f'{self._base_url}/api/songs'
        response = await self._client.post(url, json=data)
        result = response.json()
        return result.get('NewSID', '')

    async def update_song(self, sid: str, data: dict[str, Any]) -> bool:
        url = f'{self._base_url}/api/songs/sid/{sid}'
        response = await self._client.put(url, json=data)
        return response.status_code == 200

    async def close(self) -> None:
        await self._client.aclose()
