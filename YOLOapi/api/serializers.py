from rest_framework import serializers
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from menu.models import Dishes, Categories, Tables, QRCodes


User = get_user_model()


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dishes
        fields = (
            'name', 'description',
            'composition', 'price',
            'discountPrice', 'currency',
            'picture', 'categor_id',
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
            'name', 'slug'
        )

    def to_representation(self, instance):
        item = get_object_or_404(
            Categories,
            slug=super().to_representation(instance)['slug']
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
    table_id = serializers.IntegerField(source='id')

    class Meta:
        model = QRCodes
        fields = (
            'table_id',
            'qrcode'
        )
        read_only_fields = ('qrcode',)


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        fields = (
            'name',
            'email',
            'password'
        )
        model = User
