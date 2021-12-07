""" module for app specific keycloak connection """
from typing import Dict, List
import logging

from keycloak import KeycloakOpenID

from .settings import api_settings
from . import __title__

from django.http import HttpRequest

log = logging.getLogger(__title__)


def get_keycloak_openid(request: HttpRequest=None) -> KeycloakOpenID:
    server_url = api_settings.KEYCLOAK_SERVER_URL
    keycloak_realm = api_settings.KEYCLOAK_REALM
    keycloak_client_id = api_settings.KEYCLOAK_CLIENT_ID
    keycloak_client_secret_key = api_settings.KEYCLOAK_CLIENT_SECRET_KEY
    try:
        if request:
            if request.headers.get('X-KeyCloak-Server-Url'):
                server_url = request.headers['X-KeyCloak-Server-Url']

            if request.headers.get('X-KeyCloak-Realm'):
                keycloak_realm = request.headers['X-KeyCloak-Realm']

            if request.headers.get('X-KeyCloak-Client-Id'):
                keycloak_client_id = request.headers['X-KeyCloak-Client-Id']

            if request.headers.get('X-KeyCloak-Client-Secret-Key'):
                keycloak_client_secret_key = request.headers['X-KeyCloak-Client-Secret-Key']

        log.info(
            'get_keycloak_openid:'
            f'Realm={keycloak_realm}'
        )

        return KeycloakOpenID(
            server_url=server_url,
            realm_name=keycloak_realm,
            client_id=keycloak_client_id,
            client_secret_key=keycloak_client_secret_key
        )
    except KeyError as e:
        raise KeyError(
            f'invalid settings: {e}'
        )

# DEPRECATE?
#keycloak_openid = get_keycloak_openid()
keycloak_openid = None

def get_resource_roles(decoded_token: Dict) -> List[str]:
    # Get roles from access token
    resource_access_roles = []
    try:
        resource_access_roles = (
            decoded_token['resource_access']
            [api_settings.KEYCLOAK_CLIENT_ID]
            ['roles']
        )
        roles = add_role_prefix(resource_access_roles)
        log.debug(f'{__name__} - get_resource_roles - roles: {roles}')

        return roles
    except Exception as e:
        log.warn(f'{__name__} - get_resource_roles - Exception: {e}')
        return []


def add_role_prefix(roles: List[str]) -> List[str]:
    """
    add role prefix configured by KEYCLOAK_ROLE_SET_PREFIX to a list of roles
    """
    log.debug(f'{__name__} - get_resource_roles - roles: {roles}')
    prefixed_roles = [prefix_role(x) for x in roles]
    log.debug(
        f'{__name__} - get_resource_roles - prefixed_roles: {prefixed_roles}'
    )
    return prefixed_roles


def prefix_role(role: str) -> str:
    """ add prefix to role string """
    role_prefix = (
        api_settings.KEYCLOAK_ROLE_SET_PREFIX
        if api_settings.KEYCLOAK_ROLE_SET_PREFIX
        and type(api_settings.KEYCLOAK_ROLE_SET_PREFIX) is str
        else ''
    )
    return f'{role_prefix}{role}'
