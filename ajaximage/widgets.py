import os

from django.forms import widgets
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core.files.storage import get_storage_class


class AjaxImageWidget(widgets.TextInput):

    html = """
    <div class="ajaximage">
        <a class="file-link" target="_blank" href="{file_url}">
            <img class="file-img" src="{file_url}">
        </a>
        <a class="file-remove" href="#remove">Remove</a>
        <input class="file-path" type="hidden" value="{file_path}" id="{element_id}" name="{name}"/>
        <input type="file" class="file-input" />
        <input class="file-dest" type="hidden" value="{upload_url}">
        <div class="progress progress-striped active">
            <div class="bar"></div>
        </div>
    </div>
    """

    class Media:
        js = ('ajaximage/js/ajaximage.js',)
        css = {'all': ('ajaximage/css/bootstrap-progress.min.css', 'ajaximage/css/styles.css')}

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.max_width = kwargs.pop('max_width', 0)
        self.max_height = kwargs.pop('max_height', 0)
        self.crop = kwargs.pop('crop', 0)
        self.storage_path = kwargs.pop('storage_path', None)

        super(AjaxImageWidget, self).__init__(*args, **kwargs)

    # noinspection PyMethodOverriding
    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs)
        element_id = final_attrs.get('id')
        upload_to = self.upload_to
        if callable(self.upload_to):
            upload_to = self.upload_to(None, '')
        kwargs = {
            'upload_to': upload_to,
            'max_width': self.max_width,
            'max_height': self.max_height,
            'crop': self.crop,
            'storage': self.storage_path if self.storage_path is not None else '',
        }
        upload_url = reverse('ajaximage', kwargs=kwargs)
        file_path = str(value) if value else ''
        storage = get_storage_class(self.storage_path)()
        file_url = storage.url(file_path) if value else ''
        file_name = os.path.basename(file_url)
        output = self.html.format(
            upload_url=upload_url,
            file_url=file_url,
            file_name=file_name,
            file_path=file_path,
            element_id=element_id,
            name=name,
        )

        return mark_safe(output)
