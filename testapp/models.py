import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ uuid for pk """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.TextField(default=None)


class UserData(models.Model):
    """ test user data """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.TextField()
    acl = models.JSONField(default=dict)
    data = models.TextField()
