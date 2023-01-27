import requests
import json

from rest_framework import mixins, status
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from YOLOapi.settings import DOMAIN
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from menu.models import Dishes, Categories, Tables, QRCodes
from api.serializers import (
    DishSerializer, CategorySerializer,
    TableSerializer, QRCodeSerializer,
    RegisterSerializer, UserSerializer
)
from api.permissions import AdminOrSuperuser
from .functions import generate_qr


User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


def table_view(View):
    return HttpResponse()


class DishViewSet(ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class TableViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer


class RegisterViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(User, **self.kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

    def perform_create(self, serializer):
        serializer.save()


class QRCodeViewSet(CreateViewSet):
    queryset = QRCodes.objects.all()
    serializer_class = QRCodeSerializer

    def perform_create(self, serializer):
        table = get_object_or_404(Tables, id=self.request.data.get('table_id'))
        response = requests.get(DOMAIN, params={'hashsalt': table.id})
        serializer.save(
            table=table,
            qrcode=generate_qr(response.url)
        )


class ManyQRPost(ViewSet):

    def list(self, request):
        rows = Tables.objects.all()
        data = {
            'qrcodes': []
        }
        for row in rows:
            response = requests.get(DOMAIN, params={'hashsalt': row.id})
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
            response = requests.get(DOMAIN, params={'hashsalt': row.id})
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
