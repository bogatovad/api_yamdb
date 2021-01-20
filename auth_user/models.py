from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        user = 'user', _('User')
        moderator = 'moderator', _('Moderator')
        admin = 'admin', _('Admin')
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(_('email'), unique=True, db_index=True)
    role = models.CharField(max_length=10,
                            choices=RoleChoices.choices,
                            default=RoleChoices.user)

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'


User = get_user_model()
