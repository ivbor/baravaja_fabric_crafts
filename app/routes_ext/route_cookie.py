from flask import render_template, make_response

from app.app import app
from app.routes import request, jsonify


def set_cookie(cookie_name, cookie_value, response=None):

    app.logger.info(f'cookie {cookie_name} is being set to {cookie_value}')

    response = jsonify({'success': 'true'}) if response is None else response

    if not request.cookies.get(cookie_name):

        response.set_cookie(cookie_name, cookie_value)
        app.logger.info(f'cookie {cookie_name} is' +
                        f' set to {cookie_value} successfully')

        return response

    else:

        if request.cookies[cookie_name] != cookie_value:

            response.set_cookie(cookie_name, cookie_value)
            app.logger.info(f'cookie {cookie_name} is' +
                            f' set to {cookie_value} successfully')
            return response

        return jsonify({'success': 'false'})


# render_with_cookies is imported in route_admin
# that is why is goes earlier than part of import
def render_with_cookies(template, *args, **kwargs):
    app.logger.info(f'rendering {template} with {request.cookies}')
    response = make_response()
    rendered_template = render_template(template,
                                        request=request,
                                        *args,
                                        **kwargs)
    response.set_data(rendered_template)
    return response
