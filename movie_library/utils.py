from flask import make_response, current_app
from typing import Type

from movie_library import db


def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']

    return response


def populate_default_if_none(data, key, default_value):
    if data.get(key) is None:
        data[key] = default_value


def get_order_objects_list(sort_data: list, model_cls: Type[db.Model], valid_sorting_values: tuple) -> list:
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
