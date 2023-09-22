from typing import List

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class Album(SQLModel, table=True):
    __tablename__ = "albums"

    album_id: int = Field(primary_key=True)
    title: str = Field()
    year: int = Field()
    play_list_id: str = Field()
    duration: str = Field()
    duration_seconds: int = Field()
    album_cover: str = Field()
    # embedding: Optional[List[float]] = Field()
    songs: List["Song"] = Relationship(
        back_populates="album",
    )


class Song(SQLModel, table=True):
    __tablename__ = "songs"

    song_id: int = Field(primary_key=True)
    title: str = Field()
    video_id: str = Field()
    duration: str = Field()
    duration_seconds: int = Field()
    album_id: int = Field(foreign_key="albums.album_id")
    album: Album = Relationship(
        back_populates="songs",
    )
