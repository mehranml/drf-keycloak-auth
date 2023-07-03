import os
import logging
import requests
import json

from django.test import TestCase, tag
from rest_framework.test import APIClient, APITestCase
from rest_framework import status, exceptions

from settings import api_settings
from drf_keycloak_auth.keycloak import get_keycloak_openid

log = logging.getLogger('drf_keycloak_auth')


def dump(out):
    try:
        out = json.dumps(out, indent=4, sort_keys=True)
    except Exception:
        pass

    CYAN = '\033[96m'
    ENDC = '\033[0m'
    print(CYAN + str(out).replace('\\n', '\n').replace('\\t', '\t') + ENDC)


class UserLoginTestCase(APITestCase):

    # def setUp(self):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = APIClient(raise_request_exception=False)

    @tag("ok")
    def test_login_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer '
            + self.__get_token_admin(get_keycloak_openid())
        )
        response = self.client.get('/test_auth/')

        # log.debug(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("ok")
    def test_login_authentication_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'bad-token')
        response = self.client.get('/test_auth/')
        del response
        self.assertRaises(exceptions.AuthenticationFailed)

    @tag("ok", "multi")
    def test_login_multi_authentication(self):
        keycloak_openid = get_keycloak_openid(
            api_settings.KEYCLOAK_MULTI_OIDC_JSON['testserver'])

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.__get_token_admin(keycloak_openid))
        response = self.client.get('/test_auth_multi_oidc/')

        # log.debug(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("ok")
    def test_login_multi_authentication_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'bad-token')
        response = self.client.get('/test_auth_multi_oidc/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("ok")
    def test_login_multi_authentication_no_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + '')
        response = self.client.get('/test_auth_multi_oidc/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("ok")
    def test_admin_endpoint(self):
        keycloak_openid = get_keycloak_openid(
            api_settings.KEYCLOAK_MULTI_OIDC_JSON['testserver'])

        # Admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.__get_token_admin(keycloak_openid))
        response = self.client.get('/test_auth_role_admin/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.__get_token_admin(keycloak_openid))
        response = self.client.get('/test_auth_role_admin/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("ok", "user")
    def test_user_groups(self):
        keycloak_openid = get_keycloak_openid()

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer '
            + self.__get_token_user(keycloak_openid)
        )
        response = self.client.get('/test_auth/')

        # log.debug(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def __get_token_user(self, keycloak_openid):
        return self.__get_token(keycloak_openid,
                           username=os.getenv('USER_TEST_USERNAME'),
                           password=os.getenv('USER_TEST_PASSWORD')
                           )

    def __get_token_admin(self, keycloak_openid):
        return self.__get_token(keycloak_openid,
                           username=os.getenv('EC_TEST_USERNAME'),
                           password=os.getenv('EC_TEST_PASSWORD')
                           )

    def __get_token(self, keycloak_openid, username, password):
        response = requests.post(
            f'{keycloak_openid.connection.base_url}realms/'
            f'{keycloak_openid.realm_name}/protocol/openid-connect/token',
            data={
                'client_id': {keycloak_openid.client_id},
                'client_secret': {keycloak_openid.client_secret_key},
                'grant_type': 'password',
                'username': username,
                'password': password
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
        )

        dump(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['access_token'])

        return response.json()['access_token']
