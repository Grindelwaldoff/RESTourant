from django.urls import path

from api.views import (
    DishViewSet, CategoryViewSet,
    TableViewSet, CustomRegistrationViewSet,
    QRCodeViewSet, table_view,
    ManyQRPost
)


urlpatterns = [
    path('addDish/', DishViewSet.as_view({'post': 'create'})),
    path('updateDish/<int:pk>/', DishViewSet.as_view({'patch': 'update'})),
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
        CategoryViewSet.as_view({'patch': 'update'})
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
    path(
        'addWaiter/',
        CustomRegistrationViewSet.as_view({'post': 'create'})
    ),
    path(
        '', table_view, name='qr_table'
    ),
    # path('deleteWaiter/<int:pk>/', ),
    # path('authWaiter/', ),
]
