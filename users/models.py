
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from djangodirtyfield.mixin import DirtyFieldMixin


def user_photo_upload_path(instance, file):
    _, file_extension = os.path.splitext(file)
    file_path = 'users-photos/{}/profile_picture{}'.format(instance.username, file_extension)
    return file_path


class CustomUser(DirtyFieldMixin, AbstractUser):
    photo = models.ImageField(
        verbose_name=_("User photo"),
        upload_to=user_photo_upload_path,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        null=False,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
