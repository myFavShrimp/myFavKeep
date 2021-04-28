from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.authorization import jwt_authorization
from database.database import get_db
from database.operations import note as note_ops

note_id_router = APIRouter(prefix='/{note_id}', tags=['Users', 'Note Lists', 'Notes'])


@note_id_router.get('/', response_model=schema.ReadNoteList,
                    responses=response_helper.response_404)
def get_note(note_list_id: int = Path(..., description="The ID of the note list to get", ge=1),
             note_id: int = Path(..., description="The ID of the note to get", ge=1),
             current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note = note_ops.read_by_user_note_list_and_id(db, schema.UserId(id=current_user.id),
                                                     schema.NoteListId(id=note_list_id), schema.NoteId(id=note_id))

    if resp := response_helper.is_item_empty(db_note):
        return resp

    return db_note.item


@note_id_router.put('/', response_model=schema.ReadNoteList,
                    responses=response_helper.response_404)
def put_note(note: schema.UpdateNote,
             note_list_id: int = Path(..., description="The ID of the note list to update", ge=1),
             note_id: int = Path(..., description="The ID of the note to get", ge=1),
             current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note = note_ops.read_by_user_note_list_and_id(db, schema.UserId(id=current_user.id),
                                                     schema.NoteListId(id=note_list_id), schema.NoteId(id=note_id))

    if resp := response_helper.is_item_empty(db_note):
        return resp

    db_note = note_ops.update_by_id(db, schema.NoteId(id=note_id), note)
    return db_note


@note_id_router.delete('/', status_code=204,
                       responses=response_helper.response_404)
def delete_note(note_list_id: int = Path(..., description="The ID of the note list to update", ge=1),
                note_id: int = Path(..., description="The ID of the note to get", ge=1),
                current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note = note_ops.read_by_user_note_list_and_id(db, schema.UserId(id=current_user.id),
                                                     schema.NoteListId(id=note_list_id), schema.NoteId(id=note_id))

    if resp := response_helper.is_item_empty(db_note):
        return resp

    note_ops.delete_by_id(db, schema.NoteId(id=note_id))
