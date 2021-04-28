from fastapi import Path, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.authorization import jwt_authorization
from database.database import get_db
from database.operations import user as user_ops, note_list as note_list_ops


user_id_router = APIRouter(prefix='/{user_id}', tags=['Users'])


@user_id_router.get('/', response_model=schema.ReadUser,
                    responses=response_helper.response_404)
def get_user(user_id: int = Path(..., description="The ID of the user to get", ge=1),
             current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_user = user_ops.read_by_id(db, schema.UserId(id=user_id))

    if resp := response_helper.needs_access(current_user, db_user):
        return resp
    if resp := response_helper.is_item_empty(db_user):
        return resp

    return db_user.item


@user_id_router.put('/', response_model=schema.ReadUser,
                    responses=response_helper.response_404)
def put_user(user: schema.UpdateUser, user_id: int = Path(..., description="The ID of the user to update", ge=1),
             current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_user = user_ops.read_by_id(db, schema.UserId(id=user_id))

    if resp := response_helper.needs_access(current_user, db_user):
        return resp
    if resp := response_helper.is_item_empty(db_user):
        return resp
    if user_ops.is_username_taken(db, user.username, db_user.item.id):
        raise IntegrityError('', '', 'username')

    db_user = user_ops.update(db, user_id, user)
    return db_user


@user_id_router.delete('/', status_code=204,
                       responses=response_helper.response_404)
def delete_user(user_id: int = Path(..., description="The ID of the user to delete", ge=1),
                current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    db_user = user_ops.read_by_id(db, schema.UserId(id=user_id))

    if resp := response_helper.needs_access(current_user, db_user):
        return resp

    db_user = user_ops.read_by_id(db, schema.UserId(id=user_id))

    if resp := response_helper.is_item_empty(db_user):
        return resp

    # TODO delete all user notes
    note_list_ops.delete_all_by_user(db, schema.UserId(id=current_user.id))
    user_ops.delete_by_id(db, user_id)
