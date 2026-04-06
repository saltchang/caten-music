from app.core.interfaces.file_service import FileService as FileServiceInterface


class FileService:
    def __init__(self, file_service: FileServiceInterface):
        self._file_service = file_service

    async def get_ppt_url(self, sid: str) -> str | None:
        return await self._file_service.get_ppt_url(sid)

    async def get_sheet_url(self, sid: str) -> str | None:
        return await self._file_service.get_sheet_url(sid)
