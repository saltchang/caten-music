from app.core.interfaces.file_service import FileService as FileServiceInterface


class FileService:
    """Provides access to song file URLs (PPT and sheet music)."""

    def __init__(self, file_service: FileServiceInterface):
        self._file_service = file_service

    async def get_ppt_url(self, sid: str) -> str | None:
        """Get the PowerPoint file URL for a song.

        Args:
            sid: Song identifier.

        Returns:
            URL string if the file exists, None otherwise.
        """
        return await self._file_service.get_ppt_url(sid)

    async def get_sheet_url(self, sid: str) -> str | None:
        """Get the sheet music file URL for a song.

        Args:
            sid: Song identifier.

        Returns:
            URL string if the file exists, None otherwise.
        """
        return await self._file_service.get_sheet_url(sid)
