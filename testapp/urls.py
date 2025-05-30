""" api URL Configuration """
# from django.contrib import admin
from django.urls import (
    path,
    include
)
from rest_framework import routers

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path('', views.TestPublic.as_view(), name='root'),
    path('test_pub/', views.TestPublic.as_view(), name='test_pub'),
    path('test_auth/', views.TestAuth.as_view(), name='test_auth'),
    path('test_auth_multi_oidc/', views.TestAuthMultiOIDC.as_view(), name='test_auth_multi_oidc'),
    path('test_auth_role_admin/', views.TestAuthRoleAdmin.as_view(), name='test_auth_role_admin'),
    path('test_auth_role_owner/<uuid>', views.TestAuthRoleOwner.as_view(), name='test_auth_role_owner'),
    path('test_backend_call/', views.TestAuthBackendCall.as_view(), name='test_backend_call'),
    # path('admin/', admin.site.urls)

    path(
        "api-auth/", include("drf_keycloak_auth.urls", namespace='rest_framework')
    )
]
