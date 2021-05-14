import stripe

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction 
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect, JsonResponse

from .models import PizzaProduct, BeerProduct, Category, LatestProducts, Customer, Cart, CartProduct, Order
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart

from .custom_logging import logger



class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts().objects.get_products_for_main_page('pizzaproduct', 'beerproduct', with_respect_to='pizzaproduct')
        context = {
            'categories': categories,
            'products': products,
            'cart' : self.cart,
        }
        user = request.user
        logger.info('Загрузка base_view пользователем {}'.format(str(user)))
        logger.debug('Тестовое сообщение')
        return render(request, 'base.html', context)





class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'pizzaproduct': PizzaProduct,
        'beerproduct': BeerProduct
    }

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование ProductDetailView пользоватлем {user}')
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']] 
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        logger.info(f'Использование ProductDetailView get_context_data')
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context



class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        logger.info(f'Использование CategoryDetailView get_context_data')
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование AddToCartView пользоватлем {user}')
        if request.user.is_authenticated:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
            )
            if created:
                self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Товар успешно добавлен")
            return HttpResponseRedirect('/cart/')
        else:
            logger.warning('Пользователь не автоизован')
            return HttpResponseRedirect('/login/')

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование DeleteFromCartView пользоватлем {user}')
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование ChangeQTYView пользоватлем {user}')
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        return HttpResponseRedirect('/cart/')

class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование CartView пользоватлем {user}')
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование CheckOutView пользоватлем {user}')
        stripe.api_key = "sk_test_51InP7sBvCXw0ZFF356F6w3KqPuuquPMKwpfsVkFV9Rhqlq3RMCU2v476kl22BfFNbZ0efs0KTgcuw4gF8w1uV9NQ00Ajonf7zm"

        intent = stripe.PaymentIntent.create(
            amount=int(self.cart.final_price * 100),
            currency='usd',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
            'client_secret' : intent.client_secret
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование MakeOrderView пользоватлем {user}')
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, "Спасибо за заказ! Мы с вами свяжемся!")
            return HttpResponseRedirect('/')
        logger.error('Форма заказа не валидна')
        return HttpResponseRedirect('/checkout/')


class PayedOnlineOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование PayedOnlineOrderView пользоватлем {user}')
        customer = Customer.objects.get(user=request.user)
        new_order = Order()
        new_order.customer = customer
        new_order.first_name = customer.user.first_name
        new_order.last_name = customer.user.last_name
        new_order.phone = customer.phone
        new_order.address = customer.address
        new_order.buying_type = Order.BUYING_TYPE_SELF
        new_order.save()
        self.cart.in_order = True
        self.cart.save()
        new_order.cart = self.cart
        new_order.status = Order.STATUS_PAYED
        new_order.save()
        customer.orders.add(new_order)
        return JsonResponse({"status": "payed"})


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info(f'Использование LoginView')
        form = LoginForm(request.POST or None)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                logger.warning(f'Для пользователя {user} введён неправильный пароль')
        else:
            logger.warning('Форма авторизации не валидна')
        context = {'form': form,'cart': self.cart}
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info(f'Использование RegistrationView')
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {'form':form, 'categories':categories, 'cart':self.cart}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user =  form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            logger.info(f'Зарегистрирован пользователь {user}')
            return HttpResponseRedirect('/')
        logger.warning('Форма регистрации не валидна')
        context = {'form': form,'cart': self.cart}
        return render(request, 'registration.html', context)


class ProfileView(CartMixin, View):


    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'Использование ProfileView пользоватлем {user}')
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        categories = Category.objects.get_categories_for_left_sidebar()
        return render(
            request,
            'profile.html',
            {'orders':orders,'cart':self.cart, 'categories': categories}
        )
