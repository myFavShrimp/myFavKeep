from typing import NamedTuple, Optional

from sqlalchemy.orm.query import Query

from database.database import Base


class ItemList(NamedTuple):
    items: list
    total_items: int
    model: str


class SingleItem(NamedTuple):
    item: Optional[Base]
    model: str


def get_query_entity_name(query: Query) -> str:
    return str(query._primary_entity).split('->')[-1]


def read_list(query: Query) -> ItemList:
    items = query.all()
    total_items = query.count()
    model = get_query_entity_name(query)
    return ItemList(items=items, total_items=total_items, model=model)


def read_item(query: Query) -> SingleItem:
    item = query.first()
    model = get_query_entity_name(query)
    return SingleItem(item=item, model=model)


def clean_dict(dictionary: dict) -> dict:
    """
    Removes all keys from a dictionary which equal None
    """
    return {key: value for key, value in dictionary.items() if value is not None}
