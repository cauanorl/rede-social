from django import forms
from urllib import request
from django.utils.text import slugify
from django.core.files.base import ContentFile

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = {'title', 'description', 'url'}
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if valid_extensions[0] not in extension and valid_extensions[1] not in extension:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.')

        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data.get('url')
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # Faz o download da imagem a partir do URL especificado
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()

        return image
