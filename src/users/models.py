from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid

# USERNAME_REGEX = r'^[\w.@+\- ]+$'
USERNAME_REGEX = r"^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$"


class BaseUserManager(BUM):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValidationError(_("The Username must be set"))

        if not email:
            raise ValidationError(_("The Email Must be set"))

        user = self.model(username=username, email=self.normalize_email(email.lower()), **extra_fields)
        user.set_password(password)

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self.create_user(username, email, password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(
        max_length=150, unique=True, validators=[RegexValidator(regex=USERNAME_REGEX, code="invalid_username")]
    )

    email = models.EmailField(_("email address"), unique=True)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = BaseUserManager()

    def __str__(self):
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
