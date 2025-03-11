from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from rest_framework import authentication, exceptions
from requests.exceptions import HTTPError
from mozilla_django_oidc.utils import import_from_settings, parse_www_authenticate_header

from users.models import UserProfiles


class CustomAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """ Overrides Authentication Backend so that Django users are
            created with the keycloak preferred_username.
            If nothing found matching the email, then try the username.
        """
        user = super(CustomAuthenticationBackend, self).create_user(claims)
        user.first_name = claims.get('name', '').split(' ')[0]
        user.last_name = claims.get('family_name', '')
        user.email = claims.get('email')
        user.username = claims.get('email')
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """ Attempting to match users by LS AAI ID first, then by email
        """
        ls_aai_id = claims.get('sub')
        email = claims.get('email')

        users = None

        if ls_aai_id:
            # Attempting to find user with ls_aai_id first (with user profiles)
            user_profiles_check = UserProfiles.objects.filter(ls_aai_id=ls_aai_id)
            if user_profiles_check.exists():
                user_profile = UserProfiles.objects.get(ls_aai_id=ls_aai_id)
                if user_profile.user and user_profile.user.id:
                    # Finding the user associated to the found user profile
                    users = self.UserModel.objects.filter(id=user_profile.user.id)
            # Attempting to find user with email if no matching ls_aai_id in user profiles
            if not (users and users.exists()):
                if email:
                    users = self.UserModel.objects.filter(email=email)

        return users

    # def update_user(self, user, claims):
    #     user.first_name = claims.get('given_name', '')
    #     user.last_name = claims.get('family_name', '')
    #     user.email = claims.get('email')
    #     user.username = claims.get('email')
    #     user.save()
    #     return user


class CustomAuthentication(OIDCAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a tuple of (user, token) or None
        if there was no authentication attempt.
        """
        access_token = self.get_access_token(request)

        if not access_token:
            return None

        try:
            user = self.backend.get_or_create_user(access_token, None, None)
        except HTTPError as exc:
            resp = exc.response

            # if the oidc provider returns 401, it means the token is invalid.
            # in that case, we want to return the upstream error message (which
            # we can get from the www-authentication header) in the response.
            if resp.status_code == 401 and 'www-authenticate' in resp.headers:
                data = parse_www_authenticate_header(resp.headers['www-authenticate'])
                if 'error_description' in data:
                    raise exceptions.AuthenticationFailed(data['error_description'])
                #AADB2C customization
                elif 'Bearer error' in data:
                    raise exceptions.AuthenticationFailed(data['Bearer error'])

            # for all other http errors, just re-raise the exception.
            raise
        except SuspiciousOperation as exc:
            #LOGGER.info('Login failed: %s', exc)
            raise exceptions.AuthenticationFailed('Login failed')

        if not user:
            msg = 'Login failed: No user found for the given access token.'
            raise exceptions.AuthenticationFailed(msg)

        return user, access_token