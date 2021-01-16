from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(_('email'), unique=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='user')


User = get_user_model()
