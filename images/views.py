from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm


# Create your views here.
@login_required
def image_created(request):
    if request.method == "POST":
        # Formulário foi enviado
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Os dados do formulário são validos
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # Atribui o usuário atual ao item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            return redirect(new_item.get_absolute_url())
    else:
        # Cria o formulário com os dados fornecidos
        # pelo Bookmarklet via GET
        form = ImageCreateForm(request.GET)
    
    return render(request, 'images/image/create.html', {
        'section': 'images',
        'form': form,
    })
