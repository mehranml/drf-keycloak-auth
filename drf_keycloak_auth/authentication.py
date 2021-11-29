""" add a keycloak authentication class specific to Django Rest Framework """
from typing import Tuple, Dict
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser, update_last_login
from django.contrib.auth import get_user_model
from rest_framework import (
    authentication,
    exceptions,
)

from .keycloak import keycloak_openid
from .settings import api_settings
from . import __title__

log = logging.getLogger(__title__)
User = get_user_model()


class KeycloakAuthentication(authentication.TokenAuthentication):
    keyword = api_settings.KEYCLOAK_AUTH_HEADER_PREFIX

    def _get_decoded_token(self, token: str) -> str:
        """
        decode and return dict.

        TODO: can we cache well-known for faster handling?
        """
        try:
            return keycloak_openid.introspect(token)
        except Exception as e:
            raise Exception(e)

    def _verify_token_active(self, decoded_token: dict) -> None:
        """ raises if not active """
        is_active = decoded_token.get('active', False)
        if not is_active:
            raise exceptions.AuthenticationFailed(
                'invalid or expired token'
            )

    def _map_keycloak_to_django_fields(self, decoded_token: dict) -> dict:
        django_fields = {}
        keycloak_username_field = \
            api_settings.KEYCLOAK_FIELD_AS_DJANGO_USERNAME

        if (
            keycloak_username_field
            and
            type(keycloak_username_field) is str
        ):
            django_fields['username'] = \
                decoded_token.get(keycloak_username_field, '')
        django_fields['email'] = decoded_token.get('email', '')
        # django stores first_name and last_name as empty strings
        # by default, not None
        django_fields['first_name'] = \
            decoded_token.get('given_name', '')
        django_fields['last_name'] = \
            decoded_token.get('family_name', '')

        return django_fields

    def _update_user(self, user: User, django_fields: dict) -> User:
        """ if user exists, keep data updated as necessary """
        save_model = False

        for key, value in django_fields.items():
            try:
                if getattr(user, key) != value:
                    setattr(user, key, value)
                    save_model = True
            except Exception:
                log.warn(
                    'KeycloakAuthentication.'
                    '_update_user | '
                    f'setattr: {key} field does not exist'
                )
        if save_model:
            user.save()
        return user

    def _handle_local_user(self, decoded_token: dict) -> User:
        """ used to update/create local users from keycloak data """
        django_uuid_field = \
            api_settings.KEYCLOAK_DJANGO_USER_UUID_FIELD

        sub = decoded_token['sub']
        django_fields = self._map_keycloak_to_django_fields(decoded_token)

        try:
            user = User.objects.get(**{django_uuid_field: sub})
            user = self._update_user(user, django_fields)
        except ObjectDoesNotExist:
            log.warn(
                'KeycloakAuthentication._handle_local_user | '
                f'ObjectDoesNotExist: {sub} does not exist'
            )

        if user is None:
            django_fields.update(**{django_uuid_field: sub})
            user = User.objects.create_user(**django_fields)

        update_last_login(sender=None, user=user)
        return user

    def authenticate_credentials(
        self,
        token: str
    ) -> Tuple[AnonymousUser, Dict]:
        """ Attempt to verify JWT from Authorization header with Keycloak """
        log.debug('KeycloakAuthentication.authenticate_credentials')
        try:
            user = None
            # Checks token is active
            decoded_token = self._get_decoded_token(token)
            self._verify_token_active(decoded_token)
            if api_settings.KEYCLOAK_MANAGE_LOCAL_USER is not True:
                log.info(
                    'KeycloakAuthentication.authenticate_credentials: '
                    f'{decoded_token}'
                )
                user = AnonymousUser()
            else:
                user = self._handle_local_user(decoded_token)

            log.info(
                'KeycloakAuthentication.authenticate_credentials: '
                f'{user} - {decoded_token}'
            )
            return (user, decoded_token)
        except Exception as e:
            log.error(
                'KeycloakAuthentication.authenticate_credentials - '
                f'Exception: {e}'
            )
            raise exceptions.AuthenticationFailed()
