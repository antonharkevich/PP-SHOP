from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from .models import *
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class OrderInline(admin.TabularInline):
    model = Order


class CustomerAdmin(admin.ModelAdmin):
    
    inlines = [
        OrderInline
    ]


class CartProductInline(admin.TabularInline):
    model = CartProduct


class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartProductInline
    ]


class AdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px;">При загрузке изображения с разрешением больше {}x{} оно будет обрезано!</span>'.format(
            *Product.MAX_RESOLUTION
        )
        )
    
    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image .open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION 
    #     max_height, max_width = Product.MAX_RESOLUTION 
    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Размер изображения не должен быть больше, чем 3мб!')
    #     if(img.width < min_width or img.height < min_height):
    #         raise ValidationError("Разрешение изображения меньше минимального ")
    #     if(img.width > max_width or img.height > max_height):
    #         new_img = img.convert("RGB")
    #         resized_new_img = new_img.resize((150, 150), Image.ANTIALIAS)
    #         filestream = BytesIO()
    #         resized_new_img.save(filestream, 'JPEG', quality=90)
    #         filestream.seek(0)
    #         name = '{}.{}'.format(*image.name.split('.'))
    #         image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None) 
    #     return image

class PizzaAdmin(admin.ModelAdmin):
    
    form = AdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='pizza'))
        return super().formfirled_for_foreignkey(db_field, request, **kwargs)
    
    



class BeerAdmin(admin.ModelAdmin):
    
    form = AdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='beer'))
        return super().formfirled_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(PizzaProduct, PizzaAdmin)
admin.site.register(BeerProduct, BeerAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart, CartAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)