

class BaseUserException(Exception):
    default_message = None

    def __init__(self, message: str = '', *args, **kwargs) -> None:
        self.message = self.default_message if self.default_message and not message else message
        super().__init__(*args, **kwargs)


class UserCreateFailed(BaseUserException):
    default_message = 'User Creation Failed'


class UserDeleteFailed(BaseUserException):
    default_message = 'User Delete Failed'


class UserUpdateFailed(BaseUserException):
    default_message = 'User Update Failed'
