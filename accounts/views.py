from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from accounts.forms import UserSignupForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# Create your views here.
def userSignup(request):
    form = UserSignupForm()

    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)

            return HttpResponseRedirect(reverse('boards:index'))

    return render(request, 'accounts/sign-up.html',context={'form': form})

def userLogoff(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('boards:index'))

def userLogin(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('boards:index'))

    return render(request, 'accounts/login.html',context={'form':form, 'next': request.GET['next']})

class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/my-account.html'
    success_url = reverse_lazy('accounts:my-account')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user