from sqlalchemy.orm import Session

from api import schema
from database.models import Note
from database.operations import read_list, read_item, clean_dict


def create(db: Session, user: schema.UserId, note_list: schema.NoteListId, note: schema.CreateNote):
    db_note = Note(title=note.title, user_id=user.id, note_list_id=note_list.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def read_many_by_user_and_note_list(db: Session, user: schema.UserId, note_list: schema.NoteListId):
    query = db.query(Note).filter_by(user_id=user.id).filter_by(note_list_id=note_list.id)
    return read_list(query)


def read_by_user_note_list_and_id(db: Session, user: schema.UserId, note_list: schema.NoteListId, note: schema.NoteId):
    query = db.query(Note).filter_by(user_id=user.id).filter_by(note_list_id=note_list.id).filter_by(id=note.id)
    return read_item(query)


def update_by_id(db: Session, note_id: schema.NoteId, note:  schema.UpdateNote):
    query = db.query(Note).filter_by(id=note_id.id)

    updated_data = note.dict()

    updated_data = clean_dict(updated_data)
    query.update(updated_data)

    db_user = db.query(Note).filter_by(id=note_id.id).first()

    db.commit()
    return db_user


def delete_by_id(db: Session, note: schema.NoteId):
    db.query(Note).filter_by(id=note.id).delete()
    db.commit()


def delete_all_by_user(db: Session, user: schema.UserId):
    db.query(Note).filter_by(user_id=user.id).delete()
    db.commit()
