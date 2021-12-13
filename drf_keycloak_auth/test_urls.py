""" api URL Configuration """
from django.urls import (
    path,
    include
)
from rest_framework import routers

from . import test_views

router = routers.DefaultRouter()


urlpatterns = [
    path('test_auth/', test_views.TestAuth.as_view(), name='test_auth'),
    path('test_auth_multi_oidc/', test_views.TestAuthMultiOIDC.as_view(), name='test_auth_multi_oidc'),
]
