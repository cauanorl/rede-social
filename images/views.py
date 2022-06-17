from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse
from django.http import HttpResponse

from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from common.decorators import ajax_required
from actions.utils import create_action
from .forms import ImageCreateForm
from .models import Image

import redis


# Conecta com o redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


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
            create_action(request.user, "bookmarked image", new_item)
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
    # Incrementa de 1 o total de visualização da imagem
    total_views = r.incr(f'image:{image.id}:views')
    # Incrementa de 1 o ranking da imagem
    r.zincrby('image_ranking', 1, image.id)
    return render(request, 'images/image/detail.html', {
        'image': image,
        'section': 'images',
        'total_views': total_views,
    })


@login_required
def image_ranking(request):
    # Obtém o dicionário do ranking das imagens
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # Obtém as imagens mais visualizadas
    most_viewed= list(Image.objects.filter(
        id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    
    return render(request, 'images/image/ranking.html', {
        'section': 'ranking',
        'most_viewed': most_viewed,
    })


# Devolve um objeto HttpResponseNotAllowed (Código de status 405)
# Se a requisição não for do tipo POST
@login_required
@require_POST
@ajax_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = get_object_or_404(Image, id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax:
            # Se a requisição for AJAX e a página estiver fora
            # do intervalo, devolve uma página vazia
            return HttpResponse('')
        # Se a página estiver fora do intervalo,
        # exibe a última página de resultados
        images = paginator.page(paginator.num_pages)
    
    if is_ajax:
        return render(request, 'images/image/list_ajax.html', {
            'section': 'images',
            'images': images
        })
        
    return render(request, 'images/image/list.html', {
        'images': images,
        'section': 'images'
    })
