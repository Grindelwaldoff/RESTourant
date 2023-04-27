from django.urls import resolve
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import mixins, viewsets, response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser

from api.views import CreateViewSet
from superapi.serializers import (
    BusinessSerializer, UpdateSerializer, MyTokenObtainPairSerializer,
    BusinessObtainPairSerializer
)
from superapi.permissions import IsAdminOrSelf
from users.models import Business


User = get_user_model()


class WorkWithBusinessViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class BusinessUserViewSet(CreateViewSet, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = (IsAdminOrSelf,)

    def perform_create(self, serializer):
        serializer.save(
            is_business=True
        )


class BusinessViewSet(WorkWithBusinessViewSet):
    serializer_class = UpdateSerializer
    permission_classes = (IsAdminOrSelf,)

    def get_queryset(self):
        get_object_or_404(Business, business=self.kwargs.get('pk'))
        return User.objects.filter(id=self.kwargs.get('pk'))


class ListBusinessViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_business=True)
    serializer_class = UpdateSerializer
    permission_classes = (IsAdminUser,)


@api_view(['POST'])
def business_status(request, pk):
    user = get_object_or_404(User, id=pk)
    if resolve(request.path_info).url_name == 'activate_url':
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return response.Response(data={'is_active': f'{user.is_active}'}, status=status.HTTP_200_OK)


class BusinessTokenObtainPairView(TokenObtainPairView):
    serializer_class = BusinessObtainPairSerializer


class SuperUserTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
