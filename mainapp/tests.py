from decimal import Decimal
from unittest import mock
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, PizzaProduct, CartProduct, Cart, Customer
from .views import recalc_cart, AddToCartView, BaseView
from PIL import Image
from django.core.files.base import File
from io import BytesIO
from django.contrib.messages.storage.fallback import FallbackStorage


User = get_user_model()


class ShopTestCases(TestCase):

    @staticmethod
    def get_image_file(name, ext='jpeg', size=(700, 700), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password="password")
        self.category = Category.objects.create(name='Пицца', slug='pizza')
        image = self.get_image_file('pizza.jpg')
        self.pizzaproduct = PizzaProduct.objects.create(
            category = self.category,
            title = "Test pizza",
            slug = "test-slug",
            image = image,
            size = '26см',
            board = "Без борта",
            dough = 'Толстое',
            vegetarian = True,
            description= "Test description",
            price=Decimal("100.0"),
        )
        self.customer = Customer.objects.create(user=self.user, phone="1111", address="Test=Address")
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_object=self.pizzaproduct
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal("100.0"))
    
    def test_response_from_add_to_cart_view(self):
        factory = RequestFactory()
        request = factory.get('')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        response = AddToCartView.as_view()(request, ct_model="pizzaproduct", slug="test-slug")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')
    
    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('mainapp.views.BaseView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)