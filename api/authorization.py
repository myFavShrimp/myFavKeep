from fastapi_jwt_auth import AuthJWT
from fastapi import Request, Response, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth.exceptions import RevokedTokenError

from api import schema
from database.models import User
from database.operations.user import read_by_id
from database.database import get_db, with_database
from utils.configurator import get_config


def jwt_authorization(req: Request = None, res: Response = None, db: Session = Depends(get_db)):
    Authorize = AuthJWT(req, res)
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = read_by_id(db, schema.UserId(id=user_id))
    return user.item


def setup_jwt():
    @AuthJWT.load_config
    def configure():
        return get_config()

    @AuthJWT.token_in_denylist_loader
    @with_database
    def is_token_allowed(db: Session, decoded_jwt):
        db_user = db.query(User).filter_by(id=decoded_jwt['sub']).first()
        if not db_user:
            raise RevokedTokenError(401, 'Login invalid')
        if int(db_user.created_on) > decoded_jwt['iat']:
            raise RevokedTokenError(401, 'Login invalid')
        return False
