# from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel


class _BaseModel(BaseModel):
    class Config:
        orm_mode = True


# Auth

class Refresh(_BaseModel):
    access_token: str


class Login(Refresh):
    refresh_token: Optional[str]


# User

class UserId(_BaseModel):
    id: int


class LoginUser(_BaseModel):
    username: str
    password: str


class ReadUser(_BaseModel):
    id: int
    username: str
    dark_mode_enabled: bool
    is_admin: bool
    created_on: int
    updated_on: int


class CreateUser(_BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False


class UpdateUser(_BaseModel):
    id: int
    username: Optional[str]
    password: Optional[str]
    is_admin: Optional[bool]
    dark_mode_enabled: Optional[bool]


class DeleteUser(_BaseModel):
    id: int


# Note

class NoteId(_BaseModel):
    id: int


class ReadNote(_BaseModel):
    id: int
    title: str
    text: str
    user_id: int
    note_list_id: int
    created_on: int
    updated_on: int


class CreateNote(_BaseModel):
    title: str
    text: Optional[str]
    note_list_id: int


class UpdateNote(_BaseModel):
    title: Optional[str]
    text: Optional[str]
    note_list_id: Optional[int]


class DeleteNote(_BaseModel):
    id: int


# NoteList

class ReadNoteList(_BaseModel):
    id: int
    title: str
    user_id: int
    parent_note_list_id: Optional[int]
    created_on: int
    updated_on: int


class CreateNoteList(_BaseModel):
    title: str
    parent_note_list_id: Optional[int]


class UpdateNoteList(_BaseModel):
    title: Optional[str]
    parent_note_list_id: Optional[int]


class NoteListId(_BaseModel):
    id: int


# Pagination

# class PerPage(IntEnum):
#     """
#     Choices for pagination
#     """
#     ten = 10
#     twenty = 20
#     fifty = 50
#
#
# class PaginationQuery(_BaseModel):
#     page: int = 1
#     per_page: PerPage = PerPage.ten


# Lists

class ItemList(_BaseModel):
    total_items: int
    items: List


class PageWithUsers(ItemList):
    items: List[ReadUser] = []


class PageWithNotes(ItemList):
    items: List[ReadNote] = []


class PageWithNoteLists(ItemList):
    items: List[ReadNoteList] = []
