from app.core.entities.songlist import SongList
from app.core.exceptions import PermissionDeniedError, SonglistNotFoundError
from app.core.interfaces.song_api_client import SongApiClient
from app.core.interfaces.songlist_repository import SonglistRepository


class SonglistService:
    def __init__(self, songlist_repo: SonglistRepository, song_api_client: SongApiClient):
        self._songlist_repo = songlist_repo
        self._song_api_client = song_api_client

    async def create_songlist(
        self,
        user_id: int,
        title: str,
        song_sid: str | None = None,
        is_private: bool = False,
    ) -> SongList:
        songs = [song_sid] if song_sid else []
        songlist = SongList(
            id=0,
            user_id=user_id,
            title=title,
            songs_sid_list=songs,
            songs_amount=len(songs),
            is_private=is_private,
        )
        return await self._songlist_repo.create(songlist)

    async def get_songlist(self, out_id: str, user_id: int) -> SongList:
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.is_private and songlist.user_id != user_id:
            raise PermissionDeniedError('No access to this private songlist')

        return songlist

    async def get_user_songlists(self, user_id: int) -> list[SongList]:
        return await self._songlist_repo.get_by_user_id(user_id)

    async def edit_songlist(
        self,
        out_id: str,
        user_id: int,
        title: str,
        description: str,
        is_private: bool,
        is_archived: bool,
        songs_sid_list: list[str],
    ) -> SongList:
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        songlist.title = title
        songlist.description = description
        songlist.is_private = is_private
        songlist.is_archived = is_archived
        songlist.songs_sid_list = songs_sid_list
        songlist.songs_amount = len(songs_sid_list)

        return await self._songlist_repo.update(songlist)

    async def delete_songlist(self, out_id: str, user_id: int) -> None:
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        await self._songlist_repo.delete(songlist.id)

    async def toggle_song(self, out_id: str, song_sid: str, user_id: int) -> dict:
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        if song_sid in songlist.songs_sid_list:
            songlist.songs_sid_list.remove(song_sid)
            songlist.songs_amount -= 1
            action = 'remove'
        else:
            songlist.songs_sid_list.append(song_sid)
            songlist.songs_amount += 1
            action = 'add'

        await self._songlist_repo.update(songlist)

        return {'action': action, 'song_sid': song_sid, 'out_id': out_id}
