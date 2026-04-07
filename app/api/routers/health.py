from fastapi import APIRouter

router = APIRouter()


@router.get('/health')
async def health_check():
    """Return the service health status.

    Returns:
        A dict with status 'OK' when the service is running.
    """
    return {'status': 'OK'}
