from fastapi import Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.authorization import jwt_authorization
from api.endpoints.users.me.note_lists.router import note_lists_router
from database.database import get_db
from database.operations import user as user_ops, note_list as note_list_ops


me_router = APIRouter(prefix='/me', tags=['Users'])

me_router.include_router(note_lists_router)


@me_router.get('/', response_model=schema.ReadUser,
               responses=response_helper.response_404)
def get_me(current_user: jwt_authorization = Depends()):
    return current_user


@me_router.put('/', response_model=schema.ReadUser,
               responses=response_helper.response_404)
def put_me(user: schema.UpdateUser,
           current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    if user_ops.is_username_taken(db, user.username, current_user.id):
        raise IntegrityError('', '', 'username')

    db_user = user_ops.update(db, current_user.id, user)
    return db_user


@me_router.delete('/', status_code=204,
                  responses=response_helper.response_404)
def delete_me(current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    # TODO delete all user notes
    note_list_ops.delete_all_by_user(db, schema.UserId(id=current_user.id))
    user_ops.delete_by_id(db, current_user.id)
