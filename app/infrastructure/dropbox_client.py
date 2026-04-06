import asyncio

import dropbox


class DropboxFileService:
    def __init__(self, access_token: str):
        self._access_token = access_token

    def _get_dbx(self) -> dropbox.Dropbox:
        return dropbox.Dropbox(self._access_token)

    async def get_ppt_url(self, sid: str) -> str | None:
        def _fetch() -> str | None:
            dbx = self._get_dbx()
            try:
                result = dbx.files_get_temporary_link(f'/CatenMusic_Data/PPT/ppt_{sid}.ppt')
                if result is not None:
                    return result.link
            except Exception:
                pass
            try:
                result = dbx.files_get_temporary_link(f'/CatenMusic_Data/PPT/ppt_{sid}.pptx')
                if result is not None:
                    return result.link
            except Exception:
                pass
            return None

        return await asyncio.to_thread(_fetch)

    async def get_sheet_url(self, sid: str) -> str | None:
        def _fetch() -> str | None:
            dbx = self._get_dbx()
            try:
                result = dbx.files_get_temporary_link(f'/CatenMusic_Data/Sheet/{sid}.pdf')
                if result is not None:
                    return result.link
            except Exception:
                pass
            return None

        return await asyncio.to_thread(_fetch)
