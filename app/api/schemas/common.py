from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Generic response body containing a single message string."""

    message: str
