from django.db import models

# Required by create custom user model while extending the basic django feature to our model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                        PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extrafields):
        """Creates and saves new User """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extrafields)
        user.set_password(password)
        # .__db is used to support multiple data bases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates and saves a new super user"""
        user=self.create_user(email, password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Cutom suer models thst support user and email"""
    email= models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='email'

