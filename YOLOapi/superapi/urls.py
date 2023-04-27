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
        SuperUserTokenObtainPairView.as_view(),
        name='auth_admin'
    ),
    path('auth/refresh/', TokenRefreshView.as_view(),
         name='refresh_admin'),
    path(
        'authBusiness/',
        BusinessTokenObtainPairView.as_view(),
        name='business_auth'
    ),
    path('authBusiness/refresh/', TokenRefreshView.as_view(), name='business_refresh'),
    path('createBusiness/', BusinessUserViewSet.as_view({'post': 'create'}), name='create_business'),
    path('updateBusiness/<int:pk>/', BusinessViewSet.as_view(
        {'put': 'update'}
        ), name='update_Business'
    ),
    path('deleteBusiness/<int:pk>/', BusinessViewSet.as_view(
        {'delete': 'destroy'}
    ), name='delete_business'),
    path('listBusiness/', ListBusinessViewSet.as_view(
        {'get': 'list'}
    ), name='list_business'),
    path('activateBusiness/<int:pk>/', business_status, name='activate_url'),
    path(
        'deactivateBusiness/<int:pk>/',
        business_status,
        name='deactivate_url'
    ),
]
