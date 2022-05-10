from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm
from .models import Image


# Create your views here.
@login_required
def image_created(request):
    if request.method == "POST":
        # Formulário foi enviado
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Os dados do formulário são validos
            try:
                new_item = form.save(commit=False)
            except:
                messages.error(request, "This image can't be used.")
                return redirect('account:dashboard')

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


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {
        'image': image,
        'section': 'images',
    })    
