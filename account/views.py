from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse

from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.conf import settings

from common.decorators import ajax_required
from actions.utils import create_action

from . import forms
from . import models


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
            # Cria um profile para o novo usuário
            models.Profile.objects.create(user=new_user)
            create_action(new_user, "has created an account")

            return render(request, 'registration/register_done.html', {
                'new_user': new_user
            })
    else:
        user_form = forms.UserRegistrationForm()


    return render(request, 'registration/register.html', {
        'user_form': user_form,
    })


@login_required
def user_edit(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(
            data=request.POST, instance=request.user)
        profile_form = forms.ProfileEditForm(
            data=request.POST,
            instance=request.user.profile,
            files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        user_form = forms.UserEditForm(instance=request.user)
        if not getattr(request.user, 'profile', False):
            # Cria o Profile caso o usuário não o tenha
            models.Profile.objects.create(user=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def user_dashboard(request):
    return render(request, 'account/dashboard.html', {
        'section': 'dashboard'})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, "account/user/list.html", {'users': users, 'section': "people"})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "account/user/detail.html", {'user': user, 'section': 'people'})


@require_POST
@ajax_required
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                models.Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )  # Follow
                create_action(request.user, "is following", user)
            else:
                models.Contact.objects.filter(
                    user_from=request.user, user_to=user).delete()  # Unfollow
            
            return JsonResponse({'status': "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    
    return JsonResponse({"status": "error"})
