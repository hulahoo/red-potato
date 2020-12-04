from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'activation_code')


class RegisterSerializer(serializers.ModelSerializer):
    """Через этот сериалайзер у нас будут проходить данные регистрации"""
    password = serializers.CharField(min_length=1, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=1, required=True, write_only=True)

    class Meta:
        """Нужен для обозначения моделей"""
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'is_normal')

    @staticmethod
    def validate_email(value):
        """здесь мы проверяем пароли на схожесть"""
        if User.objects.filter(email=value).exists():  # здесь мы провермя на схожесть email если уже есть пользователь с таким email адресом то выкидывает следующию ошибку
            raise serializers.ValidationError('User with this email already exist')  # это ошибка выходит когда email уже занят
        return value  # возвращает value если все хорошо

    def validate(self, data):
        """здесь мы проверяем поля которые зависят друг от друрга а точнее пароль и его потдверждение. метод принимает словарь data в котором нам приходят все данные пользователя"""
        password = data.get('password')  # здесь мы получаем пароль из словаря с помощью метода get
        password_confirmation = data.pop('password_confirm')  # а здесь мы берем подтверждение пароля и если его нету то выводит None
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords does not same")
        return data


class LoginSerializer(TokenObtainPairSerializer):
    """Этот класс нужен для логина после подтверждения аккаунта"""
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)
    print('Successfully!')


class RefreshTokenSerializer(TokenRefreshSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)


    def validate(self, data):
        """Проверяем здесь на наличие пароля и почты"""
        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        print(self.context['request'])

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            print(user)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
