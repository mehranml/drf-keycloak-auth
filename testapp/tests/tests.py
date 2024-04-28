import os
import logging
import requests
import json
import urllib.parse
from django.test import TestCase, tag
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status, exceptions
from settings import api_settings
from drf_keycloak_auth.keycloak import get_keycloak_openid
from drf_keycloak_auth.clients import BackendRequestClient
from testapp.models import UserData
from .dump import dump

log = logging.getLogger('drf_keycloak_auth')

User = get_user_model()

TEST_OIDC_JSON_DEFAULT = os.getenv('TEST_OIDC_JSON_DEFAULT',
                                   'auth.dev.ecocommons.org.au')

class UserLoginTestCase(APITestCase):

    def __get_token_user(self, keycloak_openid):
        return self.__get_token(keycloak_openid,
                                username=os.getenv('USER_TEST_USERNAME'),
                                password=os.getenv('USER_TEST_PASSWORD')
                                )

    def __get_token_admin(self, keycloak_openid):
        return self.__get_token(keycloak_openid,
                                username=os.getenv('ADMIN_TEST_USERNAME'),
                                password=os.getenv('ADMIN_TEST_PASSWORD')
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

    # def setUp(self):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = APIClient(raise_request_exception=False)

    @tag("ok", "realm")
    def test_login_authentication(self):
        keycloak_openid = get_keycloak_openid()

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer '
            + self.__get_token_admin(get_keycloak_openid())
        )
        response = self.client.get('/test_auth/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure user name has realm prefix
        username = 'ecocommons-foobar:admin@example.com'

        # Ensure user realm populated
        user = User.objects.filter(username=username).first()
        dump(user)
        self.assertIsNotNone(user)
        self.assertEqual(user.realm, keycloak_openid.realm_name)

    @tag("ok")
    def test_login_authentication_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'bad-token')
        response = self.client.get('/test_auth/')
        del response
        self.assertRaises(exceptions.AuthenticationFailed)

    @tag("ok", "multi", "realm")
    def test_login_multi_authentication(self):
        keycloak_openid = get_keycloak_openid(TEST_OIDC_JSON_DEFAULT)

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.__get_token_admin(keycloak_openid))
        response = self.client.get('/test_auth_multi_oidc/')
        dump(response.data)

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
        keycloak_openid = get_keycloak_openid(TEST_OIDC_JSON_DEFAULT)

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

    @tag("ok", "data", "owner")
    def test_user_data_ownership(self):
        username = 'ecocommons-foobar:user@example.com'
        # I fetch a token
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer '
            + self.__get_token_user(get_keycloak_openid())
        )
        # and see I can login
        response = self.client.get('/test_auth/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # and get user record
        user = User.objects.filter(username=username).first()
        self.assertIsNotNone(user)
        # and create data record
        data = UserData(owner=user.id, data="some data")
        data.save()
        # and see I can access via API
        response = self.client.get('/test_auth_role_owner/'+str(data.uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('data'), "some data")

    # These dont currently run because TEST_AUTHORIZED_ENDPOINT will not run against ecocommons-foobar realm 
    @tag("ok", "clients")
    def test_backend_requests_client(self):
        keycloak_openid = get_keycloak_openid(TEST_OIDC_JSON_DEFAULT)
        base_url        = keycloak_openid.connection.base_url
        authorized_endpoint = f'{base_url}realms/{keycloak_openid.realm_name}/protocol/openid-connect/userinfo'

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.__get_token_admin(keycloak_openid))

        response = self.client.get('/test_backend_call/?url='+urllib.parse.quote(authorized_endpoint, safe=''))

        # log.debug(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    @tag("ok", "clients")
    def test_backend_requests_client_direct(self):
        keycloak_openid = get_keycloak_openid(TEST_OIDC_JSON_DEFAULT)
        base_url        = keycloak_openid.connection.base_url
        authorized_endpoint = f'{base_url}realms/{keycloak_openid.realm_name}/protocol/openid-connect/userinfo'

        client = BackendRequestClient(keycloak_openid)

        response = client.get(authorized_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.text)
