from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from . import forms


def user_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == "POST":
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Cria um objeto para o novo usuário, mas não o salva
            new_user = user_form.save(commit=False)
            # Define a senha escolhida
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Salva o objeto user
            new_user.save()
            return render(request, 'registration/register_done.html', {
                'new_user': new_user
            })
    else:
        user_form = forms.UserRegistrationForm()


    return render(request, 'registration/register.html', {
        'user_form': user_form,
    })


@login_required
def user_dashboard(request):
    return render(request, 'registration/dashboard.html', {
        'section': 'dashboard'})
