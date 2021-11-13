from flask import make_response, current_app


def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']

    return response


def populate_default_if_none(data, key, default_value):
    if data.get(key) is None:
        data[key] = default_value
