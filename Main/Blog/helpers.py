# here are the most repeated functions are here which are alwyas called.

from django.utils.text import slugify
import string
import random


def generate_random_string(N):
    res="".join(random.choices(string.ascii_lowercase + string.digits, k =N))

    return res

def generate_slug(text):
    new_slug = slugify(text)
    from Blog.models import BlogModel
    if BlogModel.objects.filter(slug=new_slug).first():
        return generate_slug(text + generate_random_string(5))
    return new_slug