import json

from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin import ModelAdmin
from django.urls import reverse


class ImageInline(GenericTabularInline):
    model = None
    extra = 0


# noinspection PyProtectedMember
class AjaxImageUploadMixin(ModelAdmin):
    change_form_template = 'ajaximage/change_form.html'
    ajax_change_form_template_extends = 'admin/change_form.html'
    image_inline = ImageInline
    upload_to = '/images/'

    def _get_context(self, request, object_id, extra_context):
        if extra_context is None:
            extra_context = {}
        data = []
        obj = self.get_object(request, object_id)
        formsets, inlines = self._create_formsets(request, obj, obj is not None)
        for inline, formset in zip(inlines, formsets):
            if hasattr(inline, 'ajax_image_upload_field'):
                upload_to = self._get_inline_upload_to(inline)
                max_width, max_height, crop, storage = self._get_inline_parameters(inline)
                url = reverse(
                    'ajaximage',
                    kwargs={
                        'upload_to': upload_to,
                        'max_width': max_width,
                        'max_height': max_height,
                        'crop': crop,
                        'storage': storage,
                    },
                )
                data.append({'ajaximage_url': url, 'prefix': formset.prefix})
        extra_context.update(
            {
                'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
                'data': json.dumps(data, ensure_ascii=False),
            }
        )
        return extra_context

    @staticmethod
    def _get_inline_parameters(inline):
        max_width = getattr(inline, 'ajax_image_max_width', 0)
        assert isinstance(max_width, int), 'ajax_image_max_width must be an integer!'
        max_height = getattr(inline, 'ajax_image_max_height', 0)
        assert isinstance(max_height, int), 'ajax_image_max_height must be an integer!'
        crop = getattr(inline, 'ajax_image_crop', 0)
        assert isinstance(crop, int), 'ajax_image_crop must be an integer!'
        storage = getattr(inline, 'ajax_image_storage_path', '')
        storage = '' if storage is None else storage
        return max_width, max_height, crop, storage

    @staticmethod
    def _get_inline_upload_to(inline):
        field = inline.model._meta.get_field(getattr(inline, 'ajax_image_upload_field'))
        upload_to = None
        if field:
            if callable(field.upload_to):
                upload_to = field.upload_to(inline.model, '').strip('/')
            else:
                upload_to = field.upload_to
        return upload_to

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self._get_context(request, object_id, extra_context=extra_context)
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = self._get_context(request, None, extra_context=extra_context)
        return super().add_view(request, form_url='', extra_context=extra_context)

    class Media:
        js = ('admin/js/jquery.init.js', 'dropzone/js/dropzone.js')
        css = {'all': ('dropzone/css/dropzone.css', 'dropzone/css/basic.css')}
