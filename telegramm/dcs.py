from dataclasses import field
from typing import ClassVar, Type, List, Optional

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = EXCLUDE

@dataclass
class MessageFrom_castom:
    id: int
    is_bot: bool
    first_name: Optional[str]


    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: Optional[str]
    username: Optional[str]
    type: str

    class Meta:
        unknown = EXCLUDE

@dataclass
class Chat_castom:
    id: int
    first_name: Optional[str]
    type: str

    class Meta:
        unknown = EXCLUDE

@dataclass
class PrivateChat(Chat):
    id: int
    first_name: str
    last_name: str
    username: str


@dataclass
class GroupChat(Chat):
    id: int
    type: str
    title: str

@dataclass
class Document:
    file_name: str
    file_id: str

@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={'data_key': 'from'})
    chat: Chat
    date: int
    video: Optional[dict]
    text: Optional[str]
    document: Optional[dict]
    photo: Optional[list]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

@dataclass
class Message_castom:
    message_id: int
    from_: MessageFrom_castom = field(metadata={'data_key': 'from'})
    chat: Chat_castom
    date: int
    video: Optional[dict]
    text: Optional[str]
    document: Optional[dict]
    photo: Optional[list]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    username: str


@dataclass
class Old_chat_member:
    user: User
    status: str

@dataclass
class New_chat_member:
    user: User
    status: str
    until_date: int



@dataclass
class My_chat_member:
    from_: MessageFrom = field(metadata={'data_key': 'from'})
    chat: Chat
    date: int
    old_chat_member: Old_chat_member
    new_chat_member: New_chat_member



    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message
    # my_chat_member: My_chat_member

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class File:
    file_id: str
    file_unique_id: str
    file_size: int
    file_path: str


@dataclass
class GetFileResponse:
    ok: bool
    result: File

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
