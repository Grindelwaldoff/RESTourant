import requests

from rest_framework import mixins, reverse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from YOLOapi.settings import DOMAIN
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from menu.models import Dish, Category, Table, QRCode
from api.serializers import (
    DishSerializer, CategorySerializer,
    TableSerializer, QRCodeSerializer,
    ManyQRSerializer
)
from api.permissions import AdminOrSuperuser
from .functions import generate_qr


class CreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


def table_view(View):
    return HttpResponse()


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class RegisterViewSet(CreateViewSet):
    pass


class QRCodeViewSet(CreateViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

    def perform_create(self, serializer):
        table = get_object_or_404(Table, id=self.request.data.get('table_id'))
        response = requests.get(DOMAIN, params={'hashsalt': table.id})
        serializer.save(
            table=table,
            qrcode=generate_qr(response.url)
        )


class ManyQRViewSet(CreateViewSet):
    queryset = QRCode.objects.all()
    serializer_class = ManyQRSerializer

    def perform_create(self, serializer):
        tables = Table.objects.all()
        for table in tables:
            response = requests.get(DOMAIN, params={'hashsalt': table.id})
            serializer.save(
                table=table,
                qrcode=generate_qr(response.url)
            )
