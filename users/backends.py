
from typing import Union
from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


class CustomModelBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None) -> Union[CustomUser, None]:
        if not ((username is None) ^ (email is None)) or password is None:
            return
        try:
            search_data = {'username': username} if email is None else {'email': email}
            user = CustomUser.objects.get(**search_data)
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user=user):
                return user

    def user_can_authenticate(self, user: CustomUser) -> bool:
        return user.is_active is True and user.is_email_verified is True
