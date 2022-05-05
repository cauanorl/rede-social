from django.shortcuts import render,HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from . import models, forms


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(
                request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponse('Authenticado')
                else:
                    return HttpResponse('Conta desativada')
            else:
                return HttpResponse('Nome ou sneha invalidos.')
    elif request.method == 'GET':
        form = forms.LoginForm()
    
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect(reverse('account:login'))


def user_register(request):
    ...


@login_required
def user_dashboard(request):
    render(request, 'account/dashboard.html', {'section': 'dashboard'})
