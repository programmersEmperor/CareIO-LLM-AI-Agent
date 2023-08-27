from pydantic import BaseModel
from Interface.Models.chatMessageModel import ChatMessage


class Body(BaseModel):
    id: int
    summary: str | None = None
    chats: list[ChatMessage]
