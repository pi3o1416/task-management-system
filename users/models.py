
import os
from django.db import models
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from dirtyfields import DirtyFieldsMixin

from .exceptions import UserUpdateFailed


def user_photo_upload_path(instance: 'CustomUser', uploaded_file: str) -> str:
    _, file_extension = os.path.splitext(uploaded_file)
    return 'users-photos/{0}/profile_picture{1}'.format(instance.username, file_extension)


class CustomUserManager(UserManager):
    pass


class CustomUser(DirtyFieldsMixin, AbstractUser):
    photo = models.ImageField(
        verbose_name=_('User Photo'),
        upload_to=user_photo_upload_path,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        _('Email'),
        blank=False,
        unique=True,
        null=False,
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=150,
        blank=True,
        default=''
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=150,
        blank=True,
        default=''
    )
    is_email_verified = models.BooleanField(
        _('Is Email Verified'),
        default=False,
    )
    is_active = models.BooleanField(
        _('Is Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = CustomUserManager()

    def save(self, *args, **kwargs) -> None:
        if self.pk is not None:
            dirty_fields = self.get_dirty_fields()
            if 'username' in dirty_fields or 'email' in dirty_fields:
                raise UserUpdateFailed(message='Username and email can not be updated')
        return super().save(*args, **kwargs)

    @property
    def full_name(self) -> str:
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __str__(self) -> str:
        return self.full_name

    def active_account(self) -> None:
        """
        Activate an user account
        """
        if self.is_active is False:
            self.is_active = True
            self.save()

    def deactivate_account(self) -> None:
        """
        Deactivate an user account
        """
        if self.is_active is True:
            self.is_active = False
            self.save()

    def grant_staff_permission(self) -> None:
        """
        Grant an user staff permission
        """
        if self.is_staff is False:
            self.is_staff = True
            self.save()

    def remove_staff_permission(self) -> None:
        """
        Remove staff permission from an user
        """
        if self.is_staff is True:
            self.is_staff = False
            self.save()

    def mark_email_verified(self) -> None:
        """
        Mark user email as verified
        """
        if self.email_verified is False:
            self.email_verified = True
            self.save()

    def mark_email_unverified(self) -> None:
        """
        Mark user email as unverified
        """
        if self.email_verified is True:
            self.email_verified = False
            self.save()

    def generate_token(self) -> str:
        """
        Generate temporary token for an user
        """
        token = default_token_generator.make_token(user=self)
        return token

    def is_token_valid(self, token: str) -> bool:
        """
        Verify a token for an user
        """
        return default_token_generator.check_token(user=self, token=token)
