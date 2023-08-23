""" api URL Configuration """
from django.urls import (
    path,
    include
)
from rest_framework import routers

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path('test_auth/', views.TestAuth.as_view(), name='test_auth'),
    path('test_auth_multi_oidc/', views.TestAuthMultiOIDC.as_view(),
         name='test_auth_multi_oidc'),
    path('test_auth_role_admin/', views.TestAuthRoleAdmin.as_view(), name='test_auth_role_admin'),
    path('test_backend_call/', views.TestAuthBackendCall.as_view(), name='test_backend_call'),
]
