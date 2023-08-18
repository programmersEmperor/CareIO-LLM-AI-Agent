from pydantic import BaseModel

from rolesEnum import Roles


class ChatMessage(BaseModel):
    role: Roles
    content: str


