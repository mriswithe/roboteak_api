from pydantic import BaseModel


class TwitchGame(BaseModel):
    name: str
    id: int
    box_art_url: str
