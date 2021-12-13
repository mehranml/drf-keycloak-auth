from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .authentication import KeycloakMultiAuthentication, KeycloakAuthentication


class test_auth(APIView):
    authentication_classes = [KeycloakAuthentication]

    def get(self, request, format=None):
        return Response({'status': 'ok'})

class test_auth_multi_oidc(APIView):
    authentication_classes = [KeycloakMultiAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        return Response({'status': 'ok'})