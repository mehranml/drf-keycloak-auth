from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from drf_keycloak_auth.clients import BackendRequestClient
from drf_keycloak_auth.authentication import KeycloakMultiAuthentication, KeycloakAuthentication
from drf_keycloak_auth import permissions as kc_permissions

class TestAuth(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'status': 'ok'})


class TestAuthMultiOIDC(APIView):
    authentication_classes = [KeycloakMultiAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'status': 'ok'})


class TestAuthRoleAdmin(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAdminUser, kc_permissions.HasAdminRole]

    def get(self, request):
        return Response({'status': 'ok'})


class TestAuthBackendCall(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client = BackendRequestClient(request.keycloak_openid)

        response = client.get(request.GET.get('url'))

        return Response(response.json(), status=response.status_code)
