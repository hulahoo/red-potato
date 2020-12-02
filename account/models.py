import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """Этот класс будет создавать запросы и самого пользоваетля"""
    def _create_user(self, email, password, **extra_fields):
        """Это служебный метод который запускается под копотом при вызове create&superuser"""
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create(self, email, password=None, **extra_fields):
        """Этот метод будет использоваться для создания пользователя"""
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Этот метод будет импользоваться для создания суперюзера"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Здесь мы моздаем этого пользователя"""
    email = models.EmailField(primary_key=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True)
    activation_code = models.CharField(max_length=36, blank=True)
    is_normal = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        """Здесь мы вывыодим читабельный текс"""
        return self.email

    def has_perm(self, perm, obj=None):
        """Проверяет на доступ только суперюзеру"""
        return self.is_active

    def has_module_perms(self, app_label):
        """Проверяет на доступ только суперюзеру"""
        return self.is_superuser

    def create_activation_code(self):
        """создаем код для регистрации"""
        activation_code = str(uuid.uuid4())
        if User.objects.filter(activation_code=activation_code):  # проверяем есть ли у другого пользователя такой же код как и у нас
            self.create_activation_code()  # то вызываем обратно этот код
        self.activation_code = activation_code  # если такого кода нету то мы его сохраняем
        self.save()
        return activation_code

    def activate_with_code(self, code):
        """здесь происходит активация с кодом"""
        if self.activation_code != code:
            raise Exception("Not Correct Activation Code")
        self.is_active = True  # после прохождения регистрации с кодом меняем пользователю состояние на True
        self.activation_code = ""  # так как код активации одноразовый мы его очищаем
        self.save()  # и здесь сохраняем пользователя


