from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from accounts.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def userSignup(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)

            return HttpResponseRedirect(reverse('boards:index'))

    return render(request, 'accounts/sign-up.html',context={'form': form})