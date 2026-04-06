import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)


async def call_church_music_api(base_url: str) -> None:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f'{base_url}/health')
            if response.status_code == 200:
                logger.info('Called church-music-api successfully')
            else:
                logger.warning('Church-music-api returned status %d', response.status_code)
    except Exception as e:
        logger.error('Error calling church-music-api: %s', e)


async def start_scheduler(base_url: str, interval_seconds: int = 300) -> None:
    logger.info('Music API Scheduler started (interval=%ds)', interval_seconds)
    await call_church_music_api(base_url)
    while True:
        await asyncio.sleep(interval_seconds)
        await call_church_music_api(base_url)
