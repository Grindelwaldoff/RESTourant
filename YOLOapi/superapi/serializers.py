from rest_framework import serializers
import webcolors
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
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


class BusinessSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    is_business = serializers.BooleanField(read_only=True)
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
        return attrs

    def perform_create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Business.objects.create(business=user)
        return user
