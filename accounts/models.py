import os
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 2541783232)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "img/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_active=True, is_staff=False):
        if not email:
            raise ValueError("Must have Email")
        if not password:
            raise ValueError("Must have password")

        user_obj = self.model(
            email=email,
            username=username
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def create_superuser(self, email,username, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,
            is_active=True,
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30)
    paypalemail = models.EmailField(max_length=500, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=500, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff
