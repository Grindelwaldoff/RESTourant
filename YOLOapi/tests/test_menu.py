from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from api import views


class AdminTest(APITestCase):

    def setUp(self) -> None:
        self.factory=APIRequestFactory
        self.view = views.DishViewSet.as_view()
        self.url = reverse('')
