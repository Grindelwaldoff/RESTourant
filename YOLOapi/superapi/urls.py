from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from .views import BusinessViewSet


urlpatterns = [
    path('auth/', TokenRefreshView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('authBusiness/', TokenObtainPairView.as_view()),
    path('authBusiness/refresh/', TokenRefreshView.as_view()),
    path('createBusiness/', BusinessViewSet.as_view({'post': 'create'})),
    # path('updateBusiness/'),
    # path('deleteBusiness/',),
    # path('listBusiness/',),
    # path('activateBusiness/<int:id>/',),
    # path('deactivateBusiness/<int:id>/',),
]
