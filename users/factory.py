
import factory
from factory.django import DjangoModelFactory
from .models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    photo = factory.django.ImageField(color='green')
    email = factory.LazyAttribute(
        lambda a: '{first_name}.{last_name}@gmail.com'.format(first_name=a.first_name, last_name=a.last_name)
    )
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.django.Password('1234')
    is_email_verified = True
    is_active = True
