import requests
import json

import base64
from rest_framework import mixins, status
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from menu.models import Dishes, Categories, Tables, QRCodes
from api.serializers import (
    DishSerializer, CategorySerializer,
    TableSerializer, QRCodeSerializer
)
from .permissions import IsBusiness
from .functions import generate_qr


User = get_user_model()


class WaiterViewSet(UserViewSet):
    permission_classes = (IsBusiness,)

    def perform_create(self, serializer):
        serializer.save(
            is_waiter=True
        )


class CreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


def table_view(View):
    return HttpResponse()


class DishViewSet(ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer
    permission_classes = (IsBusiness,)


class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsBusiness,)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj


class TableViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer
    permission_classes = (IsBusiness,)


class QRCodeViewSet(CreateViewSet):
    queryset = QRCodes.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = (IsBusiness,)

    def perform_create(self, serializer):
        table = get_object_or_404(Tables, id=self.request.data.get('table_id'))
        response = requests.get(
                self.request.build_absolute_uri(
                    f'?hashsalt={base64.b64encode(bytes(table.id))}'
                ).replace('generateQRCodes/', '')
        )
        serializer.save(
            table=table,
            qrcode=generate_qr(response.url)
        )


class ManyQRPost(ViewSet):
    permission_classes = (IsBusiness,)

    def list(self, request):
        rows = Tables.objects.all()
        data = {
            'qrcodes': []
        }
        for row in rows:
            response = requests.get(
                request.build_absolute_uri(
                    f'?hashsalt={base64.b64encode(bytes(row.id))}'
                ).replace('generateQRCodes/', '')
            )
            data['qrcodes'].append(
                {
                    'table_id': row.id,
                    'title': row.title,
                    'qrcode': generate_qr(response.url)
                }
            )
        return HttpResponse(
            json.dumps(data), content_type='application/json'
        )

    def create(self, request):
        rows = Tables.objects.all()
        data = {
            'qrcodes': []
        }
        for row in rows:
            response = requests.get(
                request.build_absolute_uri(
                    f'?hashsalt={base64.b64encode(bytes(row.id))}'
                ).replace('saveQRCodes/', '')
            )
            qrcode = generate_qr(response.url)
            data['qrcodes'].append(
                {
                    'table_id': row.id,
                    'title': row.title,
                    'qrcode': qrcode
                }
            )
            try:
                QRCodes.objects.create(
                    table=row,
                    qrcode=qrcode
                )
            except Exception:
                continue
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            status=status.HTTP_201_CREATED
        )
