from django.urls import path
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from api.views import (
    DishViewSet, CategoryViewSet,
    TableViewSet, QRCodeViewSet, table_view,
    ManyQRPost, WaiterViewSet
)


urlpatterns = [
    path('addDish/', DishViewSet.as_view({'post': 'create'})),
    path('updateDish/<int:pk>/', DishViewSet.as_view({'put': 'update'})),
    path(
        'deleteDish/<int:pk>/',
        DishViewSet.as_view({'delete': 'destroy'})
    ),
    path(
        'addCategory/',
        CategoryViewSet.as_view({'post': 'create'})
    ),
    path(
        'updateCategory/<int:pk>/',
        CategoryViewSet.as_view({'put': 'update'})
    ),
    path(
        'deleteCategory/<int:pk>/',
        CategoryViewSet.as_view({'delete': 'destroy'})
    ),
    path('addTable/', TableViewSet.as_view({'post': 'create'})),
    path(
        'deleteTable/<int:pk>/',
        TableViewSet.as_view({'delete': 'destroy'})
    ),
    path(
        'generateQRCode/',
        QRCodeViewSet.as_view({'post': 'create'})
    ),
    path(
        'generateQRCodes/', ManyQRPost.as_view({'get': 'list'})
    ),
    path(
        'saveQRCodes/', ManyQRPost.as_view({'post': 'create'})
    ),
    path('addWaiter/', WaiterViewSet.as_view({'post': 'create'})),
    path('deleteWaiter/<int:id>/', WaiterViewSet.as_view({'delete': 'destroy'})),
    path('authWaiter/', TokenObtainPairView.as_view()),
    path('authWaiter/refresh/', TokenRefreshView.as_view()),
    path(
        '', table_view, name='qr_table'
    ),
]
