from django.utils.crypto import get_random_string

import random
from string import digits


def generate_code(size, chars=digits):
    return get_random_string(size, chars)


def get_quote_code(instance, size=4, prefix='Q'):
    new_code = prefix + generate_code(size)

    q_class = instance.__class__
    if q_class.objects.filter(quote_id=new_code).exists():
        return get_quote_code(instance)

    return new_code