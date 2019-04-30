import uuid
import hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields.jsonb import JSONField

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        user = self.model(
            phone_number=phone_number,
        )

        user.set_password(password)
        print('create_user')
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number,
            password=password,
        )
        print('create_superuser')
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    phone_number = models.CharField(
        verbose_name='电话号码', max_length=20, null=True)
    name=  models.CharField(
        verbose_name='用户名', max_length=50, default='',unique=True)
    code=  models.CharField(
        verbose_name='暗号', max_length=50, default='',unique=True)
    token = models.CharField(verbose_name='token',
                                max_length=255, null=True, unique=True)
    create_time = models.DateTimeField(
    verbose_name='创建时间', auto_now_add=True, null=True)
    modify_time = models.DateTimeField(
        verbose_name='更新时间', null=True, auto_now=True)
    is_delete = models.BooleanField(verbose_name='删除标记', default=False)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def my_init(self,phone_number,name,password,role):
        self.phone_number = phone_number
        self.role_id = role
        print('set_password',password)
        self.set_password(password)
        self.name=name

    def my_init_by_openid(self, openid, password):
        self.weapp_openid = openid
        self.set_password(password)

    def get_full_name(self):
        return self.name+self.phone_number

    def get_short_name(self):
        return self.name

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin