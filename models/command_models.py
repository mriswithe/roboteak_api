from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

from twitch_enums import Roles
from .game_model import TwitchGame

if TYPE_CHECKING:
    from google.cloud.firestore_v1 import DocumentSnapshot


class Command(BaseModel):
    name: str
    template: str
    game: int = 0
    cooldown: timedelta = timedelta(seconds=5)
    required_role: Roles = Roles.GUEST

    def to_snap(self):
        vals = self.dict(exclude={"name"})
        vals["cooldown"] = vals["cooldown"].total_seconds()
        return vals

    @classmethod
    def from_snap(cls, snap: "DocumentSnapshot"):
        return cls(name=snap.id, **snap.to_dict())


class PatchCommand(BaseModel):
    name: Optional[str] = None
    game: Optional[int] = 0
    cooldown: Optional[timedelta]
    required_role: Optional[Roles]
    template: Optional[str]


class Timer(BaseModel):
    command: str
    game: Optional[TwitchGame]
    timer_frequency: int
