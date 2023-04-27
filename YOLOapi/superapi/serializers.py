from rest_framework import serializers
import webcolors
from rest_framework_simplejwt.serializers import RefreshToken, PasswordField
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.core import exceptions as django_exceptions

from users.models import Business


User = get_user_model()


class NameToHex(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.name_to_hex(data)
        except ValueError:
            raise serializers.ValidationError('Некорректное имя для цвета.')
        return data


class BusinessSerializer(UserCreateSerializer, UserSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    is_business = serializers.BooleanField(default=True, read_only=True)
    name = serializers.CharField(source='username')
    domainName = serializers.CharField(source='domain')
    ownerName = serializers.CharField(source='owner')
    ownerEmail = serializers.CharField(source='owner_email')
    ownerPhone = serializers.CharField(source='owner_phone')
    color = NameToHex(source='colors')

    class Meta:
        model = User
        fields = (
            'name', 'picture',
            'color', 'password',
            'domainName', 'ownerName',
            'ownerEmail', 'ownerPhone',
            'is_business'
        )

    def validate(self, attrs):
        user = User(attrs)
        try:
            validate_password(attrs.get('password'), user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        if User.objects.filter(domain=attrs.get('domain')).exists():
            raise serializers.ValidationError(
                {"domain": "Domain is not unique!"}
            )
        return attrs

    def perform_create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Business.objects.create(business=user)
        return user

    def to_representation(self, data):
        return {
            'id': data.id
        }


class UpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username', required=False)
    domainName = serializers.CharField(source='domain', required=False)
    ownerName = serializers.CharField(source='owner', required=False)
    ownerEmail = serializers.CharField(source='owner_email', required=False)
    ownerPhone = serializers.CharField(source='owner_phone', required=False)
    color = NameToHex(source='colors', required=False)

    class Meta(BusinessSerializer.Meta):
        fields = (
            'name', 'picture', 'color',
            'domainName', 'ownerName', 'ownerEmail',
            'ownerPhone',
        )


class SuperAdminSerializer(serializers.Serializer):
    email_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(SuperAdminSerializer, self).__init__(*args, **kwargs)

        self.fields[self.email_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        self.user = User.objects.filter(
            email=attrs[self.email_field]
        ).first()
        print(self.user)

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')
        print(self.user)
        if self.user is None or not self.user.is_active:
            raise ValidationError(
                'No active account found with the given credentials'
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` '
            'method for `MyTokenObtainSerializer` subclasses'
        )


class MyTokenObtainPairSerializer(SuperAdminSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class BusinessTokenSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['domain'] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        self.user = User.objects.filter(
            domain=attrs['domain']
        ).first()

        if self.user is None or not self.user.is_active:
            raise ValidationError(
                'No active account found with the given credentials'
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` method '
            'for `BusinessObtainPairSerializer` subclasses'
        )

class BusinessObtainPairSerializer(BusinessTokenSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(BusinessObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = f'{refresh}'
        data['access'] = f'{refresh.access_token}'

        return data
