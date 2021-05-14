from django import template
from django.utils.safestring import mark_safe
from ..custom_logging import logger

register = template.Library()


TABLE_HEAD ="""
                <table class="table">
                    <tbody>
            """


TABLE_TAIL ="""
                    </tbody>
                </table>
            """


TABLE_CONTENT = """
                    <tr>
                        <td>{name}</td>
                        <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'pizzaproduct': {
        "Размер":'size', 
        'Борт':"board", 
        "Тесто": 'dough', 
        "Вегетарианская":'vegetarian'
    },
    'beerproduct': {
        "Цвет":'colour', 
        'Крепость':"alcohol_strength", 
        "Фильтрация": 'filtered', 
        "Сорт":'grade'
    }     
}

def get_product_spec(product, model_name):
    logger.debug('Использование функции get_product_spec')
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    logger.debug('Использование функции product_spec')
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
