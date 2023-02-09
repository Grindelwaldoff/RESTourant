from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from api.views import (
    DishViewSet, CategoryViewSet,
    TableViewSet, QRCodeViewSet, table_view,
    ManyQRPost, WaiterViewSet,
    business_auth
)


urlpatterns = [
    path('auth/', business_auth),
    path('addDish/', DishViewSet.as_view({'post': 'create'}), name='add_dish'),
    path('updateDish/<int:pk>/', DishViewSet.as_view({'put': 'update'}), name='update_dish'),
    path(
        'deleteDish/<int:pk>/',
        DishViewSet.as_view({'delete': 'destroy'}),
        name='delete_dish'
    ),
    path(
        'addCategory/',
        CategoryViewSet.as_view({'post': 'create'}),
        name='add_category'
    ),
    path(
        'updateCategory/<int:pk>/',
        CategoryViewSet.as_view({'put': 'update'}),
        name='update_category'
    ),
    path(
        'deleteCategory/<int:pk>/',
        CategoryViewSet.as_view({'delete': 'destroy'}),
        name='delete_category'
    ),
    path('addTable/', TableViewSet.as_view({'post': 'create'}), name='add_table'),
    path(
        'deleteTable/<int:pk>/',
        TableViewSet.as_view({'delete': 'destroy'}),
        name='delete_table'
    ),
    path(
        'generateQRCode/',
        QRCodeViewSet.as_view({'post': 'create'}),
        name='generate_code'
    ),
    path(
        'generateQRCodes/', ManyQRPost.as_view({'get': 'list'}),
        name='generate_codes'
    ),
    path(
        'saveQRCodes/', ManyQRPost.as_view({'post': 'create'}),
        name='save_codes'
    ),
    path('addWaiter/', WaiterViewSet.as_view({'post': 'create'}), name='add_waiter'),
    path(
        'deleteWaiter/<int:id>/',
        WaiterViewSet.as_view({'delete': 'destroy'}),
        name='delete_waiter'
    ),
    path('authWaiter/', TokenObtainPairView.as_view(), name='auth_waiter'),
    path('authWaiter/refresh/', TokenRefreshView.as_view(), name='refresh_waiter'),
    path(
        '', table_view, name='qr_table'
    ),
]
