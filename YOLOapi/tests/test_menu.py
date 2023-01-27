import shutil
import tempfile

from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from menu.models import Dish, Category


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class TestModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.category = Category.objects.create(
            name='Супы',
            slug='soups'
        )
        cls.dish = Dish.objects.create(
            name='Буябес1',
            description='Изысканный суп',
            composition='свекла, сметана, говядина',
            price=1000,
            discountPrice=700,
            currency='RUB',
            picture=uploaded,
            category_id=cls.category,
            is_popular=True
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_dish_verbose(self):
        field_verbose_name = {
            'name': 'Наименование:',
            'description': 'Описание:',
            'composition': 'Состав блюда:',
            'price': 'Цена блюда:',
            'discountPrice': 'Дисконтная цена:',
            'currency': 'Валюта:',
            'picture': 'Внешний вид блюда:',
            'category_id': 'Категория блюда:',
            'is_popular': 'Востребованность блюда:'
        }
        for field, expected_value in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.dish._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_dish(self):
        dish_count = Dish.objects.count()
        small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        Dish.objects.create(
            name='Буябес',
            description='Изысканный суп',
            composition='свекла, сметана, говядина',
            price=1000,
            discountPrice=700,
            currency='RUB',
            picture=uploaded,
            category_id=self.category,
            is_popular=True
        )
        self.assertEqual(Dish.objects.count(), dish_count+1)

    def test_category(self):
        cat_count = Category.objects.count()
        Category.objects.create(
            name='Второе',
            slug='lunch'
        )
        self.assertEqual(
            Category.objects.count(),
            cat_count+1
        )
