import requests

from app.routes_ext.route_cookie import set_cookie


def get_user_location(app, ip_address):
    app.logger.info('trying to get location of the user' +\
                    f'with ip {ip_address}')
    try:
        response = requests.get(
            f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        return data.get("country")
    except Exception as e:
        app.logger.info(f"Error getting location: {e}")
        return None


def map_location_to_language(location):
    language_mapping = {
        "US": "en",
        "UK": "en",
        "RU": "ru",
        "UA": "ru",
        "BY": "ru",
        "PL": "pl"
        # Add more mappings as needed
    }
    return language_mapping[location]


def get_user_language(app, request):

    try:
        # from cookies
        if request.cookies.get('user_language'):
            app.logger.info('getting user language from cookies')
            return request.cookies.get('user_language')
        # from browser
        elif request.headers.get("Accept-Language"):
            app.logger.info('getting user language from browser')
            user_languages = request.headers.get("Accept-Language")
            user_language = user_languages.split(
                ',')[0].split(';')[0]
            set_cookie('user_language',
                       user_language if user_language else 'en')
            return user_language
        # from location
        else:
            ip_address = request.remote_addr
            user_location = get_user_location(app, ip_address)
            if user_location:
                return map_location_to_language(user_location)
            else:
                return "en"
    except Exception as e:
        app.logger.info(f"Error getting user language: {e}")
        return "en"
