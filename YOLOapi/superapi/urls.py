from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from superapi.views import (
    BusinessViewSet,
    BusinessUserViewSet,
    ListBusinessViewSet,
    business_status,
    SuperUserTokenObtainPairView,
    BusinessTokenObtainPairView
)


urlpatterns = [
    path(
        'auth/',
        SuperUserTokenObtainPairView.as_view()
    ),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path(
        'authBusiness/',
        BusinessTokenObtainPairView.as_view()
    ),
    path('authBusiness/refresh/', TokenRefreshView.as_view()),
    path('createBusiness/', BusinessUserViewSet.as_view({'post': 'create'})),
    path('updateBusiness/<int:pk>/', BusinessViewSet.as_view(
        {'put': 'update'}
    )),
    path('deleteBusiness/<int:pk>/', BusinessViewSet.as_view(
        {'delete': 'destroy'}
    )),
    path('listBusiness/', ListBusinessViewSet.as_view(
        {'get': 'list'}
    )),
    path('activateBusiness/<int:pk>/', business_status, name='activate_url'),
    path(
        'deactivateBusiness/<int:pk>/',
        business_status,
        name='deactivate_url'
    ),
]
