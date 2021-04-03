from django import template
import urllib, hashlib
from myproject.settings import STATIC_URL

register = template.Library()
@register.filter
def gravatar(user):
    email = user.email.encode()
    print(type(email))

    #TODO: Understand why the author made the choices he did for implementation in the tutorial
    default = "https://www.example.com/default.jpg"
    size = 256

    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email).hexdigest() + "?"
    gravatar_url += urllib.parse.urlencode({'s': str(size)})

    return gravatar_url