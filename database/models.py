from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
import time

from database.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    password_hash = Column(String(), nullable=False)
    dark_mode_enabled = Column(Integer, default=1, nullable=False)
    is_admin = Column(Integer, default=0, nullable=False)

    created_on = Column(Float, default=time.time)
    updated_on = Column(Float, default=time.time, onupdate=time.time)


class NoteList(Base):
    __tablename__ = 'note_list'

    id = Column(Integer, primary_key=True)
    title = Column(String())

    user_id = Column(Integer, ForeignKey('user.id'))
    parent_note_list_id = Column(Integer, ForeignKey('note_list.id'))

    user = relationship('User', backref="note_lists")
    parent_note_list = relationship('NoteList', remote_side=[id], backref='sub_note_lists')

    created_on = Column(Float, default=time.time)
    updated_on = Column(Float, default=time.time, onupdate=time.time)


class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    text = Column(String())

    user_id = Column(Integer, ForeignKey('user.id'))
    note_list_id = Column(Integer, ForeignKey('note_list.id'))

    user = relationship('User', backref="files")
    note_list = relationship('NoteList', backref='notes')

    created_on = Column(Float, default=time.time)
    updated_on = Column(Float, default=time.time, onupdate=time.time)
