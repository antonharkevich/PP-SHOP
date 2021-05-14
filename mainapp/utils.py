from django.db import models
from .custom_logging import logger
def recalc_cart(cart):
    logger.info('Использование функции recalc_cart')
    cart_data =  cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price =  cart_data.get('final_price__sum')
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()