import logging

from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from jose import jwt
from jwt import PyJWKClient
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from mozilla_django_oidc.utils import import_from_settings, parse_www_authenticate_header
import requests
from rest_framework import authentication, exceptions

from configs.identity_config import *
from users.models.users import Users


logger = logging.getLogger('django')
logger = logging.getLogger('mozilla_django_oidc')


class CustomAuthenticationBackend(OIDCAuthenticationBackend):
    def __init__(self):
        super().__init__()
        # Entra-specific discovery
        self.discovery = requests.get(DISCOVERY_URL).json()
        self.jwks_client = PyJWKClient(self.discovery['jwks_uri'])
        self.issuer = self.discovery['issuer']
        self.audience = f"{CLIENT_ID}"
        
    def validate_access_token(self, access_token):
        # Get signing key from Entra JWKS
        signing_key = self.jwks_client.get_signing_key_from_jwt(access_token)
        
        # Full Entra JWT validation
        claims = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=self.audience,
            issuer=self.issuer,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
            }
        )

        # Validate required scope
        if 'access_as_user' not in claims.get('scp', '').split():
            raise exceptions.AuthenticationFailed('Missing required scope')
        
        return claims

    def get_or_create_user(self, access_token, id_token, payload):
        # Override, passing claims through "payload"
        """Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched."""

        """ Skip call to Graph API and get claims from access_token """
        # user_info = self.get_userinfo(access_token, id_token, payload)
        # claims_verified = self.verify_claims(user_info)
        # if not claims_verified:
        #     msg = "Claims verification failed"
        #     raise SuspiciousOperation(msg)

        users = self.filter_users_by_claims(payload)

        if len(users) == 1:
            return self.update_user(users[0], payload)
        elif len(users) > 1:
            # In the rare case that two user accounts have the same email address,
            # bail. Randomly selecting one seems really wrong.
            msg = "Multiple users returned"
            raise SuspiciousOperation(msg)
        elif self.get_settings("OIDC_CREATE_USER", True):
            user = self.create_user(payload)
            return user
        else:
            logger.debug(
                "Login failed: No user with %s found, and OIDC_CREATE_USER is False",
                self.describe_user_by_claims(payload),
            )
            return None
    
    def create_user(self, claims):
        # Override
        user = super(CustomAuthenticationBackend, self).create_user(claims) # TODO: ?
        user.username = claims.get('oid')   # OID is the immutable identifier for an object in the Microsoft identity system (same across applications)
        user.email = claims.get('email')
        user.last_name = claims.get('name', '')
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """ Attempting to match users by Microsoft OID first, then by email
        """
        oid = claims.get('oid')
        email = claims.get('email')

        users = None

        # This function should return a list of Users (list of len 0 or 1)
        if oid:
            users = Users.objects.filter(username=oid)
            if not users.exists():
                users = Users.objects.filter(email=email)

        return users

    def update_user(self, user, claims):
        user.username = claims.get('oid')
        user.email = claims.get('email')
        user.last_name = claims.get('name', '')
        user.save()
        return user


class CustomAuthentication(OIDCAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a tuple of (user, token) or None
        if there was no authentication attempt.
        """
        access_token = self.get_access_token(request)

        if not access_token:
            raise exceptions.AuthenticationFailed('Invalid token')

        claims = self.backend.validate_access_token(access_token)

        if not claims:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        try:
            user = self.backend.get_or_create_user(access_token, None, claims)
            # self.get_or_create_user(None, id_token, None)
        except SuspiciousOperation as exc:
            #LOGGER.info('Login failed: %s', exc)
            raise exceptions.AuthenticationFailed('Login failed')

        if not user:
            msg = 'Login failed: No user found for the given access token.'
            raise exceptions.AuthenticationFailed(msg)

        return user, access_token
            