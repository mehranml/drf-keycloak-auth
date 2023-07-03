from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from drf_keycloak_auth.authentication import KeycloakMultiAuthentication, KeycloakAuthentication


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
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response({'status': 'ok'})