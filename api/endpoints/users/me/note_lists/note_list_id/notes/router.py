from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.authorization import jwt_authorization
from api.endpoints.users.me.note_lists.note_list_id.notes.note_id.router import note_id_router
from database.operations import note as note_ops
from database.database import get_db


notes_router = APIRouter(prefix='/notes', tags=['Users', 'Note Lists', 'Notes'])

notes_router.include_router(note_id_router)


@notes_router.get('/', response_model=schema.PageWithNotes,
                  responses=response_helper.response_404)
def get_notes(note_list_id: int = Path(..., description="The ID of the note list to get", ge=1),
              current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_notes = note_ops.read_many_by_user_and_note_list(db, schema.UserId(id=current_user.id),
                                                        schema.NoteListId(id=note_list_id))

    if resp := response_helper.is_item_empty(db_notes):
        return resp

    return db_notes


@notes_router.post('/', response_model=schema.ReadNoteList, status_code=201,
                   responses=response_helper.response_409)
def post_note(note: schema.CreateNote,
              note_list_id: int = Path(..., description="The ID of the note list to get", ge=1),
              current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    return note_ops.create(db, schema.UserId(id=current_user.id), schema.NoteListId(id=note_list_id), note)
