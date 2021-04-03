import django.test as test
import django.shortcuts as shortcuts

def fn1():

    url = shortcuts.reverse('accounts:sign-up')
    data = {
        'username': 'NewUser'
        , 'password1': 'BananaGrapevine99'
        , 'password2': 'BananaGrapevine99'
    }

    client = test.Client()
    response = client.post(url,data)
    print(response.context['form'])