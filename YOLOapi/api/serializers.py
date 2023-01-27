from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, validators

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


class UserBaseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    name = serializers.CharField(
        max_length=150,
        validators=[
            validators.UnicodeUsernameValidator(),
        ]
    )

    class Meta:
        model = User
        fields = ('name', 'email')

    def validate(self, attrs):
        if not User.objects.filter(**attrs).exists() and self.is_valid():
            self.validated_data({'name': attrs.get('name')})
            self.validated_data({'email': attrs.get('email')})
        return attrs

    def validate_attribute(self, attr):
        if User.objects.filter(**attr).exists():
            raise serializers.ValidationError(
                f'User with name {attr} exists!'
            )

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        return user


class UserSerializer(UserBaseSerializer):
    login = serializers.CharField(source='name')

    class Meta(UserBaseSerializer.Meta):
        fields = (
            'login',
        )


class RegisterSerializer(UserBaseSerializer):

    class Meta(UserBaseSerializer.Meta):
        fields = (
            'name',
            'email'
        )


# class TokenObtainPairSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True)

#     class Meta:
#         fields = ('name', 'confirmation_code')
#         model = Token

#     def validate(self, attrs):
#         user = get_object_or_404(User,
#                                  username=attrs.get(
#                                      'username'))
#         if not (user.auth_token.key == attrs.get(
#                 'confirmation_code')):
#             raise serializers.ValidationError(
#                 'Confirmation code is invalid.')
#         return user
