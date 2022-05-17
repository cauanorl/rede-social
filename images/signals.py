from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image

"""  
@receiver: decorador para indicar que é uma função receptora
m2m_changed: O sinal só será enviado quando um ManyToManyField é alterado
sender: O campo que será verificado
"""
@receiver(m2m_changed, sender=Image.users_like.through)  # .through -> Devolve o objeto imagem baseado nesse campo
def user_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
