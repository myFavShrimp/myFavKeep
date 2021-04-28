import re
from typing import List, Dict, Union

from pydantic import BaseModel
from fastapi.responses import JSONResponse

from database.operations import ItemList, SingleItem
from database.models import User as UserObject


def _split_at_uppercase(string: str):
    return re.findall('[A-Z][^A-Z]*', string)


class _Login(BaseModel):
    detail: List[Dict[str, str]] = [{'msg': 'Login not correct'}]


class _Permissions(BaseModel):
    detail: List[Dict[str, str]] = [{'msg': 'Insufficient permissions'}]


class _Detail(BaseModel):
    detail: List[Dict[str, str]] = [{'msg': '{item} not found'}]


class _DetailWithLoc(BaseModel):
    detail: List[Dict[str, str]] = [{'loc': ['location', 'value'],
                                     'msg': 'already exists'}]


response_401 = {401: {"model": _Login}}
response_403 = {403: {"model": _Permissions}}
response_404 = {404: {"model": _Detail}}
response_409 = {409: {"model": _DetailWithLoc}}


def is_item_empty(item: Union[ItemList, SingleItem]):
    """
    :return: fastapi JSONResponse if the item is empty, None if it has data
    """
    model = item.model
    if type(item) == SingleItem and (not item.item):
        item_title = str(model)
    elif type(item) == ItemList and (not item.items):
        apostrophe = "'"  # backslashes are not allowed in fstring expressions
        item_title = f'{str(type(item).__name__)} with {str(model).lower()}' \
                     f'{apostrophe if str(model).endswith("s") else "s"}'
    else:  # item(s) not empty
        return
    return JSONResponse(status_code=404, content={'detail': [{'msg': f'{item_title} not found'}]})


_insufficient_permissions_response = JSONResponse(status_code=403,
                                                  content={'detail': [{'msg': 'Insufficient permissions'}]})


def needs_admin(user_to_check: UserObject):
    """
    Checks if 'user_to_check' is an admin.
    :param user_to_check: The user to check.
    :return: 'JSONResponse' if the user is not an admin.
    """
    if not user_to_check.is_admin:
        print("lol")
        return _insufficient_permissions_response


def needs_ownership(user_to_check: UserObject, resource_to_check: Union[ItemList, SingleItem]):
    """
    Check if the user owns or is the resource.
    :param user_to_check: The user to check.
    :param resource_to_check: The resource to check for.
    :return: 'JSONResponse' if the user is not an admin or the resource.
    """
    if not user_to_check == resource_to_check.item:
        if not user_to_check.id == resource_to_check.item.user_id:
            return _insufficient_permissions_response


def needs_access(user_to_check: UserObject, resource_to_check: Union[ItemList, SingleItem]):
    """
    Checks if the user is admin or owns the resource. .
    :param user_to_check: The user to check.
    :param resource_to_check: The resource to check for.
    :return: 'JSONResponse' if not the user should not have access.
    """
    if resp := needs_ownership(user_to_check, resource_to_check):
        if resp := needs_admin(user_to_check):
            return resp
