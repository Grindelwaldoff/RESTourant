from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField
from django.shortcuts import get_object_or_404

from menu.models import Dish, Category, Table, QRCode


class DishSerializer(ModelSerializer):

    class Meta:
        model = Dish
        fields = (
            'name', 'description',
            'composition', 'price',
            'discountPrice', 'currency',
            'picture', 'category_id',
            'is_popular'
        )

    def to_representation(self, instance):
        item = get_object_or_404(
            Dish,
            name=super().to_representation(instance)['name']
        )
        instance = {'id': item.id}
        return instance


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'name', 'slug'
        )

    def to_representation(self, instance):
        item = get_object_or_404(
            Category,
            slug=super().to_representation(instance)['slug']
        )
        return {'id': item.id}


class TableSerializer(ModelSerializer):

    class Meta:
        model = Table
        fields = (
            'id',
            'title',
        )


class QRCodeSerializer(ModelSerializer):
    table_id = IntegerField(source='id')

    class Meta:
        model = QRCode
        fields = (
            'table_id',
            'qrcode'
        )
        read_only_fields = ('qrcode',)


class ManyQRSerializer(ModelSerializer):
    table_id = RelatedField(queryset=Table)

    class Meta:
        model = QRCode
        fields = (
            'table_id',
            'qrcode'
        )
        read_only_fields = ('qrcode',)

    # def to_representation(self, instance):
    #     tables = get_object_or_404(Table)
    #     qrcodes = get_object_or_404(QRCode)
    #     res = {
    #         'qrcodes': [
                
    #         ]
    #     }
    #     for qrcode in qrcodes:
    #         res.get('qrcodes').append(
    #             {
    #                 'table_id': tables.filter(id=qrcode.table),
    #                 'table_title': tables.get(id=qrcode.table).title,
    #                 'qr_code': qrcode.qrcode,
    #             }
    #         )
    #     return res
 