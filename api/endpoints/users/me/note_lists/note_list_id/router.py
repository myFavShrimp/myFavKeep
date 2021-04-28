from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.authorization import jwt_authorization
from api.endpoints.users.me.note_lists.note_list_id.notes.router import notes_router
from database.database import get_db
from database.operations import note_list as note_list_ops


note_list_id_router = APIRouter(prefix='/{note_list_id}', tags=['Users', 'Note Lists'])

note_list_id_router.include_router(notes_router)


@note_list_id_router.get('/', response_model=schema.ReadNoteList,
                         responses=response_helper.response_404)
def get_note_list(note_list_id: int = Path(..., description="The ID of the note list to get", ge=1),
                  current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note_list = note_list_ops.read_by_user_and_id(db, schema.NoteListId(id=note_list_id),
                                                     schema.UserId(id=current_user.id))

    if resp := response_helper.is_item_empty(db_note_list):
        return resp

    return db_note_list.item


@note_list_id_router.put('/', response_model=schema.ReadNoteList,
                         responses=response_helper.response_404)
def put_note_list(note_list: schema.UpdateNoteList,
                  note_list_id: int = Path(..., description="The ID of the note list to update", ge=1),
                  current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note_list = note_list_ops.read_by_user_and_id(db, schema.NoteListId(id=note_list_id),
                                                     schema.UserId(id=current_user.id))

    if resp := response_helper.is_item_empty(db_note_list):
        return resp

    db_note_list = note_list_ops.update_by_id(db, schema.NoteListId(id=note_list_id), note_list)
    return db_note_list


@note_list_id_router.delete('/', status_code=204,
                            responses=response_helper.response_404)
def delete_note_list(note_list_id: int = Path(..., description="The ID of the note list to update", ge=1),
                     current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note_lists = note_list_ops.read_by_user_and_id(db, schema.NoteListId(id=note_list_id),
                                                      schema.UserId(id=current_user.id))

    if resp := response_helper.is_item_empty(db_note_lists):
        return resp

    note_list_ops.delete_by_id(db, schema.NoteListId(id=note_list_id))
