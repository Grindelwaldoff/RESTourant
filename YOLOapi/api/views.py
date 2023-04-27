import requests
import json

from rest_framework import mixins, status, exceptions, generics
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend

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


class TableList(generics.ListAPIView):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hashsalt',]
    permission_classes = (IsBusiness,)


def perform_create(self, serializer):
    if self.request.user.is_business or self.request.user.is_superuser:
        serializer.save(
            business=self.request.user
        )
    else:
        raise exceptions.AuthenticationFailed(
            {'error': 'User is not a business.'}
        )


class DishViewSet(ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer
    permission_classes = (IsBusiness,)

    def perform_create(self, serializer):
        return perform_create(self, serializer)


class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsBusiness,)

    def perform_create(self, serializer):
        return perform_create(self, serializer)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj


class TableViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer
    permission_classes = (IsBusiness,)

    def perform_create(self, serializer):
        return perform_create(self, serializer)


class QRCodeViewSet(CreateViewSet):
    queryset = QRCodes.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = (IsBusiness,)

    def perform_create(self, serializer):
        table = Tables.objects.filter(hashsalt=self.request.data.get('table_id')).first()
        response = requests.get(
                self.request.build_absolute_uri(
                    f'?hashsalt={table.hashsalt}'
                    # f'?hashsalt={base64.b64encode(bytes(table.hashsalt)).decode("utf-8")}'
                ).replace('generateQRCode/', '')
        )
        if self.request.user.is_business or self.request.user.is_superuser:
            serializer.save(
                business=self.request.user,
                table=table,
                qrcode=generate_qr(response.url),
            )
        else:
            raise exceptions.AuthenticationFailed(
                {'error': 'User is not a business.'}
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
                    f'?hashsalt={row.hashsalt}'
                    # f'?hashsalt={base64.b64encode(bytes(row.hashsalt)).decode("utf-8")}'
                ).replace('generateQRCodes/', '')
            )
            data['qrcodes'].append(
                {
                    'table_id': row.id,
                    'title': row.title,
                    'qrcode': generate_qr(response.url)['image_base64']
                }
            )
        return HttpResponse(
            json.dumps(data), content_type='application/json'
        )

    def perform_create(self, serializer):
        return perform_create(self, serializer)

    def create(self, request):
        rows = Tables.objects.all()
        data = {
            'qrcodes': []
        }
        for row in rows:
            response = requests.get(
                request.build_absolute_uri(
                    f'?hashsalt={row.hashsalt}'
                    # f'?hashsalt={base64.b64encode(bytes(row.hashsalt)).decode("utf-8")}'
                ).replace('saveQRCodes/', '')
            )
            qrcode = generate_qr(response.url)
            data['qrcodes'].append(
                {
                    'table_id': row.id,
                    'title': row.title,
                    'qrcode': qrcode['image_base64']
                }
            )
            QRCodes.objects.get_or_create(
                table=row,
                business=request.user,
                qrcode=qrcode['image_base64']
            )
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            status=status.HTTP_201_CREATED
        )


def business_auth(request):
    return redirect('business_auth')
