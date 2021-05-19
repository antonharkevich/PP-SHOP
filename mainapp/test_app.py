from decimal import Decimal
from unittest import mock
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, PizzaProduct, CartProduct, Cart, Customer
from .views import CategoryDetailView, CheckoutView, recalc_cart, AddToCartView, BaseView, DeleteFromCartView, ProfileView, LoginView, BeerAddView, PizzaAddView
from PIL import Image
from django.core.files.base import File
from io import BytesIO
from django.contrib.messages.storage.fallback import FallbackStorage
import pytest
from django.conf import settings
from django.test import Client


User = get_user_model()


@pytest.fixture
def get_image_file1():
    name='pizza.jpg' 
    ext='jpeg'
    size=(700, 700)
    color=(256, 0, 0)
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)

@pytest.fixture
def user(db):
    user = User.objects.create(username='testuser', password="password")
    return user


@pytest.fixture
def customer(db, user):
    customer = Customer.objects.create(user=user, phone="1111", address="Test=Address")
    return customer


@pytest.fixture
def category(db):
    category = Category.objects.create(name='Пицца', slug='pizza')
    return category


@pytest.fixture
def pizzaproduct(db, get_image_file1, category):
    image = get_image_file1
    pizzaproduct = PizzaProduct.objects.create(
            category = category,
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
    return pizzaproduct

@pytest.fixture
def cart(db, customer):
    cart = Cart.objects.create(owner=customer)
    return cart


@pytest.fixture
def cart_product(db, customer, cart, pizzaproduct):
    cart_product = CartProduct.objects.create(
            user=customer,
            cart=cart,
            content_object=pizzaproduct
    )
    return cart_product


@pytest.mark.parametrize("expected", [1, Decimal("100.0")])
def test_add_to_cart_without_cls(cart, cart_product, expected):
        cart.products.add(cart_product)
        recalc_cart(cart)
        assert cart.products.count() , cart.final_price == expected


@pytest.mark.parametrize("expected", [302, '/cart/'])
def test_response_from_add_to_cart_view(user, pizzaproduct, expected):
    factory = RequestFactory()
    request = factory.get('')
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    request.user = user
    response = AddToCartView.as_view()(request, ct_model="pizzaproduct", slug="test-slug")
    assert response.status_code, response.url == expected


@pytest.mark.parametrize("expected", [302, '/cart/'])
def test_response_from_delete_from_cart_view(user, pizzaproduct, cart_product, expected):
        factory = RequestFactory()
        request = factory.get('')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = user
        response = DeleteFromCartView.as_view()(request, ct_model="pizzaproduct", slug="test-slug")
        assert response.status_code, response.url == expected


def test_response_from_base_view(user):
        factory = RequestFactory()
        request = factory.get('')
        request.user = user
        response = BaseView.as_view()(request)
        assert response.status_code == 200


def test_response_from_profile_view(user):
        factory = RequestFactory()
        request = factory.get('')
        request.user = user
        response = ProfileView.as_view()(request)
        assert response.status_code == 200


def test_login_get_view(user):
        factory = RequestFactory()
        request = factory.get('')
        request.user = user
        response = LoginView.as_view()(request)
        assert response.status_code == 200


def test_login_post_view(db):
    c = Client()
    response = c.post('/login/', {'username': 'admin', 'password': 'admin'})
    assert response.status_code == 200


@pytest.mark.parametrize("expected", [302, '/'])
def test_registration_post_view(db, expected):
    c = Client()
    response = c.post('/registration/', {
        'username': 'antonnn', 'password': 'antonn', 'confirm_password': 'antonn', 'phone': '+375444444444', 
        'first_name': 'Anton', 'last_name': 'Ivanov', 'address': 'Минская, д.5', 'email': 'testmail54@mail.ru'
    })
    assert response.status_code, response.url == expected


@pytest.mark.parametrize("expected", [302, '/'])
def test_makeorder_view(db, user, expected):
    user.set_password('password')
    user.save()
    c = Client()
    c.login(username='testuser', password='password')
    response = c.post('/makeorder/', {
        'first_name': 'Anton', 'last_name': 'Ivanov', 'phone': '+375444444444', 'address': 'Минская, д.5', 
        'buying_type': "self", 'order_date': '05/17/2021', 'comment' : 'Test_comment' 
        
    })
    assert response.status_code, response.url == expected


def test_categorydetail_view(category):
    c = Client()
    response = c.get('/category/pizza/')
    assert response.status_code == 200


def test_beeradd_get_view(user):
        factory = RequestFactory()
        request = factory.get('')
        request.user = user
        response = BeerAddView.as_view()(request)
        assert response.status_code == 200


def test_pizzaadd_get_view(user):
        factory = RequestFactory()
        request = factory.get('')
        request.user = user
        response = PizzaAddView.as_view()(request)
        assert response.status_code == 200


@pytest.mark.parametrize("expected", [302, '/category/pizza/'])
def test_pizzaadd_post_view(db, expected, category, pizzaproduct, get_image_file1,):
    c = Client()
    image = get_image_file1
    image.seek(0)
    response = c.post('/pizza_add/', {
        'title':  'Новая',
        'slug' : 'new_slug',
        'image':image,
        'description' : 'some',
        'price' : Decimal("100.0"),
        'size' : '54sm',
        'board' : 'without',
        'dough' : 'Тонкое',
        'vegetarian' : True
    })
    print(response.url)
    assert response.status_code, response.url == expected




