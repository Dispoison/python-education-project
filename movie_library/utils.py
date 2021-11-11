from flask import make_response, current_app


def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']

    return response
