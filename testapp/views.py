from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions
from drf_keycloak_auth.clients import BackendRequestClient
from drf_keycloak_auth.authentication import (
    KeycloakSessionAuthentication,
    KeycloakMultiAuthentication,
    KeycloakAuthentication,
)
from drf_keycloak_auth.keycloak import get_keycloak_openid
from drf_keycloak_auth import permissions as kc_permissions
from testapp.models import UserData


class TestPublic(APIView):
    authentication_classes = [KeycloakMultiAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class TestAuth(APIView):
    authentication_classes = [KeycloakAuthentication, KeycloakSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"status": "ok", "user": str(request.user), "auth": request.auth})


class TestAuthMultiOIDC(APIView):
    authentication_classes = [KeycloakMultiAuthentication, KeycloakSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"status": "ok", "user": str(request.user), "auth": request.auth})


class TestAuthRoleAdmin(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAdminUser, kc_permissions.HasAdminRole]

    def get(self, request):
        return Response({"status": "ok", "auth": request.auth})


class TestAuthBackendCall(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client = BackendRequestClient(request.keycloak_openid)
        response = client.get(request.GET.get("url"))
        return Response(response.json(), status=response.status_code)


class TestAuthRoleOwner(GenericAPIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAuthenticated, kc_permissions.HasOwnerRole]
    queryset = UserData.objects.all()
    lookup_field = "uuid"

    def get(self, request, uuid):
        userdata = self.get_object()
        return Response({"uuid": userdata.uuid, "data": userdata.data})
