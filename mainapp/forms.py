from django import forms
from django.contrib.auth.models import User
from .models import Order, PizzaProduct
from .custom_logging import logger

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields["password"].label = "Пароль"

    def clean(self):
        logger.info('Проверка авторизации пользователя')
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            logger.error(f"Пользователь с логином {username} не найден в системе.")
            raise forms.ValidationError(f"Пользоватеь с логином {username} не найден в системе.")
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                logger.error(f"Для пользователя с логином {username} введен неверный пароль")
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data


    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address =  forms.CharField(required=False)
    email = forms.EmailField(required=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields["password"].label = "Пароль"
        self.fields['confirm_password'].label = "Подтвердите пароль"
        self.fields["phone"].label = "Номер телефона"
        self.fields['first_name'].label = "Ваше имя"
        self.fields["last_name"].label = "Ваша фамилия"
        self.fields['address'].label = "Адрес"
        self.fields['email'].label = "Электронная почта"

    def clean_email(self):
        logger.info('Проверка почты при регистрации пользователя')
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net']:
            logger.error(f'Регистрация для домена "{domain}" невозможна')
            raise forms.ValidationError(f'Регистрация для домена "{domain}" невозможна')
        if User.objects.filter(email=email).exists():
            logger.error(f"Данный почтовый адрес {email} уже зарегестрирован в системе")
            raise forms.ValidationError(f"Данный почтовый адрес уже зарегестрирован в системе")
        return email
    
    def clean_username(self):
        logger.info('Проверка логина при регистрации пользователя')
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            logger.error(f'Имя {username} занято')
            raise forms.ValidationError(f'Имя {username} занято')
        return username
    
    def clean(self):
        logger.info('Проверка пароля при регистрации пользователя')
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            logger.error('Пароли не совпадают!')
            raise forms.ValidationError('Пароли не совпадают!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']


class PizzaAddForm(forms.ModelForm):


    title = forms.CharField(max_length=255)
    slug = forms.SlugField()
    image = forms.ImageField(allow_empty_file=True, required=False)
    description = forms.CharField()
    price = forms.DecimalField(max_digits=9, decimal_places=2)
    size = forms.CharField(max_length=255)
    board = forms.CharField(max_length=255)
    dough = forms.CharField(max_length=255)
    vegetarian = forms.BooleanField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Наименование"
        self.fields["slug"].label = "Slug"
        self.fields['image'].label = "Изображение"
        self.fields["description"].label = "Описание"
        self.fields['price'].label = "Цена"
        self.fields["size"].label = "Размер"
        self.fields['board'].label = "Борт"
        self.fields['dough'].label = "Тесто"
        self.fields['vegetarian'].label = "Вегетарианская"


    class Meta:
        model = PizzaProduct
        fields = (
            'title', 'slug', 'image', 'description', 'price', 'size', 'board', 'dough', 'vegetarian'
        )


class BeerAddForm(forms.ModelForm):


    title = forms.CharField(max_length=255)
    slug = forms.SlugField()
    image = forms.ImageField()
    description = forms.CharField()
    price = forms.DecimalField(max_digits=9, decimal_places=2)
    colour = forms.CharField(max_length=255)
    alcohol_strength = forms.CharField(max_length=255) 
    filtered = forms.CharField(max_length=255)
    grade = forms.CharField(max_length=255)  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Наименование"
        self.fields["slug"].label = "Slug"
        self.fields['image'].label = "Изображение"
        self.fields["description"].label = "Описание"
        self.fields['price'].label = "Цена"
        self.fields["colour"].label = "Цвет"
        self.fields['alcohol_strength'].label = "Крепость"
        self.fields['filtered'].label = "Фильтрация"
        self.fields['grade'].label = "Сорт"


    class Meta:
        model = PizzaProduct
        fields = (
            'title', 'slug', 'image', 'description', 'price', 'colour', 'alcohol_strength', 'filtered', 'grade'
        )


        
