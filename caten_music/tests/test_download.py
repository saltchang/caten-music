# tests/test_download.py

from . import client

import pytest

download_params = [("1", "很抱歉，這首詩歌目前沒有投影片資料可供下載", "Redirecting"),
                   ("-1", "很抱歉，這首詩歌目前沒有投影片資料可供下載", "Redirecting"),
                   ("0", "很抱歉，這首詩歌目前沒有投影片資料可供下載", "Redirecting"),
                   ("1010066", "Redirecting", "很抱歉，這首詩歌目前沒有投影片資料可供下載"),
                   ("2010010", "Redirecting", "很抱歉，這首詩歌目前沒有投影片資料可供下載"),
                   ("0010030", "很抱歉，這首詩歌目前沒有投影片資料可供下載", "Redirecting"),
                   ("0000000", "很抱歉，這首詩歌目前沒有投影片資料可供下載", "Redirecting"),
                   ("abc", "很抱歉，這首詩歌目前沒有投影片資料可供下載", "Redirecting"),
                   ("", "404", "Redirecting")]


@pytest.mark.parametrize("id_, ex, nex", download_params)
def test_download_ppt(client, id_, ex, nex):
    """測試下載功能"""

    res = client.get("/downloadppt/" + id_)
    res = res.data.decode()

    assert ex in res
    assert nex not in res
