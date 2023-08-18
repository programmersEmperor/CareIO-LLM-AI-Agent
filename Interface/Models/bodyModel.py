from pydantic import BaseModel
from Interface.Models.chatMessageModel import ChatMessage


class Body(BaseModel):
    summary: str | None = None
    chats: list[ChatMessage]
