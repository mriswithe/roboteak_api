from datetime import datetime

from pydantic import BaseModel

from twitch_enums import Roles


class BaseUser(BaseModel):
    login: str
    user_id: int
    role: Roles


class ChatUser(BaseUser):
    minutes: int


class WebUser(BaseUser):
    expires_at: datetime
    refresh_token: str
    access_token: str
    token_type: str
    login_uuid: str
