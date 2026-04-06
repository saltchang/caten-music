from typing import Any

from app.core.interfaces.song_api_client import SongApiClient


class SongService:
    def __init__(self, song_api_client: SongApiClient):
        self._song_api_client = song_api_client

    async def search(self, mode: str, query: str) -> list[dict[str, Any]]:
        if mode == 'title':
            return await self._song_api_client.search(title=query)
        elif mode == 'lyric':
            return await self._song_api_client.search(lyrics=query)
        return []

    async def browse(
        self,
        lang: str = '',
        collection: str = '',
        tonality: str = '',
    ) -> list[dict[str, Any]]:
        return await self._song_api_client.search(lang=lang, collection=collection, tonality=tonality)

    async def get_by_sid(self, sid: str) -> list[dict[str, Any]]:
        return await self._song_api_client.get_by_sid(sid)

    async def get_by_sids(self, sids: list[str]) -> list[dict[str, Any]]:
        return await self._song_api_client.get_by_sids(sids)

    async def get_random(self, amount: int = 6) -> list[dict[str, Any]]:
        return await self._song_api_client.get_random(amount)

    async def create_song(self, data: dict[str, Any]) -> str:
        return await self._song_api_client.create_song(data)

    async def update_song(self, sid: str, data: dict[str, Any]) -> bool:
        return await self._song_api_client.update_song(sid, data)
