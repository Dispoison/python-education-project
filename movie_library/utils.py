"""Application utilities"""

from typing import Type, List, Callable
from datetime import datetime
from functools import wraps
from re import search

from flask import abort
from flask_login import current_user, login_user

from movie_library import db
from movie_library.models import User


class AuthenticationError(Exception):
    """Exception raised when authentication failed for some reason."""


def get_order_objects_list(sort_data: List[str], model_cls: Type[db.Model],
                           valid_sorting_values: tuple) -> list:
    """Gets order objects from sort data"""
    order_by = []

    if sort_data:
        for sort_value in sort_data:
            sort_attr_and_mode = sort_value.split(',')
            if len(sort_attr_and_mode) == 1:
                sort_attr_and_mode.append('desc')
            sort_attr, mode = sort_attr_and_mode

            if sort_attr in valid_sorting_values:
                if mode == 'asc':
                    order_by.append(getattr(model_cls, sort_attr))
                elif mode == 'desc':
                    order_by.append(getattr(model_cls, sort_attr).desc())
                else:
                    raise ValueError(f'Incorrect input: sorting mode parameter \'{mode}\'. '
                                     f'Use \'asc\' or \'desc\' -  by default.')
            else:
                raise ValueError(f'Incorrect input: sort parameter \'{sort_attr}\'. '
                                 f'Valid sorting parameters - {", ".join(valid_sorting_values)}.')
    else:
        order_by.append(None)

    return order_by


def verify_ownership_by_user_id(user_id: int, error_message: str):
    """Checks ownership of current user according to user_id or if admin"""
    if not (current_user.is_admin or current_user.id == user_id):
        return abort(403, error_message)


def admin_required(function: Callable):
    """Decorator raises 403 exception if current user is not admin"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return abort(403, 'Not enough rights.')
        return function(*args, **kwargs)
    return wrapper


def unauthorized_required(function: Callable):
    """Decorator raises 403 exception if current user is not admin"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return abort(400, f'You are already logged in as {current_user.username}.')
        return function(*args, **kwargs)
    return wrapper


def get_all_or_404(model_cls: Type[db.Model], not_found_msg: str) -> List[db.Model]:
    """Gets list of objects and raises 404 exception if list is empty"""
    objects = model_cls.query.all()
    if not objects:
        return abort(404, not_found_msg)
    return objects


def add_model_object(object_: db.Model):
    """Adds model object to database"""
    db.session.add(object_)
    db.session.commit()


def update_model_object(object_: db.Model):
    """Updates model object"""
    db.session.commit()


def delete_model_object(object_: db.Model):
    """Deletes model object"""
    db.session.delete(object_)
    db.session.commit()


def refresh_and_login_user(user: User):
    """Updates user last activity and log in"""
    user.last_activity = datetime.now()
    db.session.commit()
    login_user(user)


def parse_column_name_from_message_detail(message_detail):
    return search(r'\((.*?)\)', message_detail).group(1)
