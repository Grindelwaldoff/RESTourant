from django.contrib.auth import get_user_model

from api.views import CreateViewSet
from superapi.serializers import BusinessSerializer


User = get_user_model()


class BusinessViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = BusinessSerializer

    def perform_create(self, serializer):
        serializer.save(
            is_business=True
        )
