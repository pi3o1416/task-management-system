
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from dirtyfields import DirtyFieldsMixin


def user_photo_upload_path(instance: 'CustomUser', uploaded_file: str) -> str:
    _, file_extension = os.path.splitext(uploaded_file)
    return 'users-photos/{0}/profile_picture{1}'.format(instance.username, file_extension)


class CustomUser(DirtyFieldsMixin, AbstractUser):
    photo = models.ImageField(
        verbose_name=_('User photo'),
        upload_to=user_photo_upload_path,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        null=False,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    @property
    def full_name(self) -> str:
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __str__(self) -> str:
        return self.full_name
