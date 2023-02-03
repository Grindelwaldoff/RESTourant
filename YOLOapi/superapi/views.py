from rest_framework import viewsets
from django.contrib.auth import get_user_model

from business.models import Business
from .serializers import BusinessSerializer


User = get_user_model()


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
