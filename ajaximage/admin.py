import json

from django.contrib.contenttypes.admin import GenericTabularInline

from adminsortable.admin import SortableGenericTabularInline, NonSortableParentAdmin


class ImageInline(SortableGenericTabularInline, GenericTabularInline):
    model = None
    extra = 0


class AjaxImageUploadMixin(NonSortableParentAdmin):
    change_form_template = 'ajaximage/change_form.html'
    ajax_change_form_template_extends = 'adminsortable/change_form.html'
    image_inline = ImageInline
    upload_to = '/images/'

    def _get_context(self, request, object_id, extra_context):
        if extra_context is None:
            extra_context = {}
        data = []
        obj = self.get_object(request, object_id)
        formsets, inlines = self._create_formsets(request, obj,not obj is None)
        for inline, formset in zip(inlines, formsets):
            if hasattr(inline, 'ajax_image_upload_field'):
                field = inline.model._meta.get_field(getattr(inline, 'ajax_image_upload_field'))
                upload_to = None
                if field:
                    if callable(field.upload_to):
                        upload_to = field.upload_to(inline.model, '').strip('/')
                    else:
                        upload_to = field.upload_to
                data.append({
                    'upload_to': upload_to,
                    'prefix': formset.prefix,
                })
        extra_context.update({
            'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
            'data': json.dumps(data, ensure_ascii=False),
        })
        return extra_context

    # noinspection PyProtectedMember
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self._get_context(request, object_id, extra_context=extra_context)
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)

    # noinspection PyProtectedMember
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = self._get_context(request, None, extra_context=extra_context)
        return super().add_view(request, form_url='', extra_context=extra_context)

    class Media:
        js = (
            'dropzone/js/dropzone.js',
        )
        css = {
            'all': (
                'dropzone/css/dropzone.css',
                'dropzone/css/basic.css',
            )
        }
