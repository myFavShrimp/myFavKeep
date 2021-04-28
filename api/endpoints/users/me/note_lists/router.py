from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.authorization import jwt_authorization
from api.endpoints.users.me.note_lists.note_list_id.router import note_list_id_router
from database.database import get_db
from database.operations import note_list as note_list_ops


note_lists_router = APIRouter(prefix='/note_lists', tags=['Users', 'Note Lists'])

note_lists_router.include_router(note_list_id_router)


@note_lists_router.get('/', response_model=schema.PageWithNoteLists,
                       responses=response_helper.response_404)
def get_note_lists(current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_note_lists = note_list_ops.read_many_by_user(db, schema.UserId(id=current_user.id))

    if resp := response_helper.is_item_empty(db_note_lists):
        return resp

    return db_note_lists


@note_lists_router.post('/', response_model=schema.ReadNoteList, status_code=201,
                        responses=response_helper.response_409)
def post_note_list(note_list: schema.CreateNoteList,
                   current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    return note_list_ops.create(db, schema.UserId(id=current_user.id), note_list)
