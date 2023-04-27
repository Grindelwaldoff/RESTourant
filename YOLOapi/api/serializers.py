from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users.models import Waiter

from menu.models import Dishes, Categories, Tables, QRCodes


User = get_user_model()


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dishes
        fields = (
            'name', 'description',
            'composition', 'price',
            'discountPrice', 'currency',
            'picture', 'category_id',
            'is_popular'
        )

    def to_representation(self, instance):
        item = get_object_or_404(
            Dishes,
            name=super().to_representation(instance)['name']
        )
        instance = {'id': item.id}
        return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = (
            'name',
        )

    def to_representation(self, instance):
        item = get_object_or_404(
            Categories,
            name=super().to_representation(instance)['name']
        )
        return {'id': item.id}


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tables
        fields = (
            'id',
            'title',
        )


class QRCodeSerializer(serializers.ModelSerializer):
    table_id = serializers.IntegerField(source='table')

    class Meta:
        model = QRCodes
        fields = (
            'table_id',
            'qrcode'
        )
        read_only_fields = ('qrcode',)


class CustomRegistartionSerializer(UserCreateSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    is_waiter = serializers.BooleanField(read_only=True)
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = (
            'name', 'email',
            'password', 'is_admin',
            'is_waiter'
        )

    def validate(self, attrs):
        super().validate(attrs)
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError(
                'User with this email already exists.'
            )
        return attrs

    def to_representation(self, data):
        return {
            'id': data.id
        }

    def perform_create(self, validated_data):
        user = super().perform_create(validated_data)
        if user.is_waiter:
            Waiter.objects.create(waiter=user)
        return user
