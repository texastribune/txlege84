from social.backends.oauth import BaseOAuth2


class TribOAuth2(BaseOAuth2):
    """Texas Tribune OAuth authentication backend"""
    name = 'texastribune'
    AUTHORIZATION_URL = 'https://www.texastribune.org/oauth2/authorize/'
    ACCESS_TOKEN_URL = 'https://www.texastribune.org/oauth2/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'email'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('expires_in', 'expires_in')
    ]

    def get_user_details(self, response):
        """Return user details from Texas Tribune account"""
        return {
            'username': response.get('username'),
            'email': response.get('email') or '',
            'first_name': response.get('first_name') or '',
            'last_name': response.get('last_name') or '',
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""

        result = self.get_json(
            'https://www.texastribune.org/api/self/',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
        return result
