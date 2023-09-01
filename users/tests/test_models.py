
import factory
import factory.random
from django.test import TestCase

from ..models import CustomUser
from ..factories import CustomUserFactory
from ..exceptions import UserUpdateFailed


class CustomUserTest(TestCase):
    def setUp(self) -> None:
        factory.random.reseed_random('users')
        CustomUserFactory.create(username='testuser')

    def test_photo_field(self) -> None:
        photo_field = CustomUser._meta.get_field('photo')
        self.assertTrue(photo_field.null, 'Photo field null should be allowed')
        self.assertTrue(photo_field.blank, 'Photo field blank should be True')
        self.assertEqual(photo_field.verbose_name, 'User Photo', 'Photo field verbose name did not match')

    def test_photo_field_upload_path(self) -> None:
        user: CustomUser = CustomUser.objects.get(username='testuser')
        photo_field = CustomUser._meta.get_field('photo')
        upload_path: str = photo_field.upload_to(user, 'test.png')
        self.assertEqual(upload_path, 'users-photos/{username}/profile_picture.png'.format(username=user.username))

    def test_email_field(self) -> None:
        email_field = CustomUser._meta.get_field('email')
        self.assertEqual(email_field.verbose_name, 'Email', 'Email field verbose name did not match')
        self.assertFalse(email_field.null, 'Email field should be null restricted')
        self.assertFalse(email_field.blank, 'Email field should be blank restricted')
        self.assertTrue(email_field.unique, 'Email field shoulb be unique')

    def test_first_name_field(self) -> None:
        first_name_field = CustomUser._meta.get_field('first_name')
        self.assertEqual(first_name_field.verbose_name, 'First Name', 'First name field verbose name did not match')
        self.assertEqual(first_name_field.max_length, 150, 'Max length should be 150')
        self.assertEqual(first_name_field.default, '', 'Default value on first name field did not match')
        self.assertTrue(first_name_field.blank, 'Blank value on first name should be allowed')

    def test_last_name_field(self) -> None:
        last_name_field = CustomUser._meta.get_field('last_name')
        self.assertEqual(last_name_field.verbose_name, 'Last Name', 'Last name field verbose name did not match')
        self.assertEqual(last_name_field.max_length, 150, 'Max length should be 150')
        self.assertEqual(last_name_field.default, '', 'Default value on last name field did not match')
        self.assertTrue(last_name_field.blank, 'Blank value on last name should be allowed')

    def test_email_verified_field(self) -> None:
        email_verified_field = CustomUser._meta.get_field('is_email_verified')
        self.assertEqual(email_verified_field.verbose_name, 'Is Email Verified', 'Verbose name did not match')
        self.assertEqual(email_verified_field.default, False, 'Initially default value should be False')

    def test_is_active_field(self) -> None:
        active_field = CustomUser._meta.get_field('is_active')
        self.assertEqual(active_field.default, True, 'Initially default value should be True')
        self.assertEqual(active_field.verbose_name, 'Is Active', 'Verbose Name did not matched')

    def test_username_update_restriction(self) -> None:
        try:
            user: CustomUser = CustomUser.objects.get(username='testuser')
            user.username = 'newusername'
            user.save()
            raise Exception
        except Exception as exception:
            self.assertTrue(
                isinstance(exception, UserUpdateFailed),
                'Username update is not restricted'
            )

    def test_email_update_restriction(self) -> None:
        try:
            user: CustomUser = CustomUser.objects.get(username='testuser')
            user.email = 'newemail@gmail.com'
            user.save()
            raise Exception
        except Exception as exception:
            self.assertTrue(
                isinstance(exception, UserUpdateFailed),
                'Email update is not restricted'
            )

    def test_full_name_property(self) -> None:
        user: CustomUser = CustomUser.objects.get(username='testuser')
        self.assertEqual(
            user.full_name, '{first_name} {last_name}'.format(first_name=user.first_name, last_name=user.last_name),
            'Full name property is not working'
        )

    def test_token_validation(self) -> None:
        user1: CustomUser = CustomUserFactory.create()
        user2: CustomUser = CustomUserFactory.create()
        user1_token = user1.generate_token()
        user2_token = user2.generate_token()
        self.assertTrue(user1.is_token_valid(user1_token), 'Token should be valid')
        self.assertFalse(user1.is_token_valid(user2_token), 'Token should be invalid')
        self.assertFalse(user2.is_token_valid(user1_token), 'Token should be invalid')
