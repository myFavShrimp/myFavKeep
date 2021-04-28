from sqlalchemy.orm import Session

from api import schema
from database.models import NoteList
from database.operations import read_list, read_item, clean_dict


def create(db: Session, user: schema.UserId, note_list: schema.CreateNoteList):
    db_note_list = NoteList(title=note_list.title, user_id=user.id, parent_note_list_id=note_list.parent_note_list_id)
    db.add(db_note_list)
    db.commit()
    db.refresh(db_note_list)
    return db_note_list


def read_many_by_user(db: Session, user: schema.UserId):
    query = db.query(NoteList).filter(NoteList.user_id == user.id)
    return read_list(query)


def read_by_user_and_id(db: Session, note_list: schema.NoteListId, user: schema.UserId):
    query = db.query(NoteList).filter_by(user_id=user.id).filter_by(id=note_list.id)
    return read_item(query)


def update_by_id(db: Session, note_list_id: schema.NoteListId, note_list: schema.UpdateNoteList):
    db_user_query = db.query(NoteList).filter_by(id=note_list_id.id)

    updated_data = note_list.dict()

    updated_data = clean_dict(updated_data)
    db_user_query.update(updated_data)

    db_user = db.query(NoteList).filter_by(id=note_list_id).first()

    db.commit()
    return db_user


def delete_by_id(db: Session, note_list: schema.NoteListId):
    db.query(NoteList).filter_by(id=note_list.id).delete()
    db.commit()


def delete_all_by_user(db: Session, user: schema.UserId):
    db.query(NoteList).filter_by(user_id=user.id).delete()
    db.commit()
