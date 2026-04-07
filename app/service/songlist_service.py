from app.core.entities.songlist import SongList
from app.core.exceptions import PermissionDeniedError, SonglistNotFoundError
from app.core.interfaces.songlist_repository import SonglistRepository


class SonglistService:
    """Manages songlist CRUD and song toggling within playlists."""

    def __init__(self, songlist_repo: SonglistRepository) -> None:
        self._songlist_repo = songlist_repo

    async def create_songlist(
        self,
        user_id: int,
        title: str,
        song_sid: str | None = None,
        is_private: bool = False,
    ) -> SongList:
        """Create a new songlist, optionally seeded with one song.

        Args:
            user_id: Owning user's ID.
            title: Songlist title.
            song_sid: Initial song SID to include (optional).
            is_private: Whether the songlist is private.

        Returns:
            The created SongList entity with generated out_id.
        """
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
        """Fetch a songlist, enforcing private access control.

        Args:
            out_id: External songlist ID.
            user_id: Requesting user's ID.

        Returns:
            The SongList entity.

        Raises:
            SonglistNotFoundError: If songlist does not exist.
            PermissionDeniedError: If songlist is private and user is not the owner.
        """
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.is_private and songlist.user_id != user_id:
            raise PermissionDeniedError('No access to this private songlist')

        return songlist

    async def get_user_songlists(self, user_id: int) -> list[SongList]:
        """Fetch all songlists belonging to a user.

        Args:
            user_id: The user's primary key.

        Returns:
            List of the user's SongList entities.
        """
        return await self._songlist_repo.get_by_user_id(user_id)

    async def edit_songlist(
        self,
        out_id: str,
        user_id: int,
        title: str | None = None,
        description: str | None = None,
        is_private: bool | None = None,
        is_archived: bool | None = None,
        songs_sid_list: list[str] | None = None,
    ) -> SongList:
        """Partially update a songlist. Only non-None fields are applied.

        Args:
            out_id: External songlist ID.
            user_id: ID of the requesting user (ownership check).
            title: New title, if provided.
            description: New description, if provided.
            is_private: New privacy flag, if provided.
            is_archived: New archived flag, if provided.
            songs_sid_list: New song list, if provided.

        Returns:
            Updated SongList entity.

        Raises:
            SonglistNotFoundError: If songlist does not exist.
            PermissionDeniedError: If user is not the owner.
        """
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        if title is not None:
            songlist.title = title
        if description is not None:
            songlist.description = description
        if is_private is not None:
            songlist.is_private = is_private
        if is_archived is not None:
            songlist.is_archived = is_archived
        if songs_sid_list is not None:
            songlist.songs_sid_list = songs_sid_list
            songlist.songs_amount = len(songs_sid_list)

        return await self._songlist_repo.update(songlist)

    async def delete_songlist(self, out_id: str, user_id: int) -> None:
        """Delete a songlist owned by the user.

        Args:
            out_id: External songlist ID.
            user_id: Requesting user's ID (ownership check).

        Raises:
            SonglistNotFoundError: If songlist does not exist.
            PermissionDeniedError: If user is not the owner.
        """
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        await self._songlist_repo.delete(songlist.id)

    async def add_song(self, out_id: str, song_sid: str, user_id: int) -> SongList:
        """Add a song to a songlist (idempotent).

        Args:
            out_id: External songlist ID.
            song_sid: Song SID to add.
            user_id: ID of the requesting user.

        Returns:
            Updated SongList entity.

        Raises:
            SonglistNotFoundError: If songlist does not exist.
            PermissionDeniedError: If user is not the owner.
        """
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        if song_sid not in songlist.songs_sid_list:
            songlist.songs_sid_list.append(song_sid)
            songlist.songs_amount += 1
            await self._songlist_repo.update(songlist)

        return songlist

    async def remove_song(self, out_id: str, song_sid: str, user_id: int) -> SongList:
        """Remove a song from a songlist (idempotent).

        Args:
            out_id: External songlist ID.
            song_sid: Song SID to remove.
            user_id: ID of the requesting user.

        Returns:
            Updated SongList entity.

        Raises:
            SonglistNotFoundError: If songlist does not exist.
            PermissionDeniedError: If user is not the owner.
        """
        songlist = await self._songlist_repo.get_by_out_id(out_id)
        if not songlist:
            raise SonglistNotFoundError('Songlist not found')

        if songlist.user_id != user_id:
            raise PermissionDeniedError('Not the owner of this songlist')

        if song_sid in songlist.songs_sid_list:
            songlist.songs_sid_list.remove(song_sid)
            songlist.songs_amount -= 1
            await self._songlist_repo.update(songlist)

        return songlist
