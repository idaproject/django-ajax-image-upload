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

    # noinspection PyProtectedMember
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context.update({
            'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
        })
        extra_context.update({
            'upload_to': self.upload_to.strip('/'),
        })
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)

    # noinspection PyProtectedMember
    def add_view(self, request, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context.update({
            'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
        })
        extra_context.update({
            'upload_to': self.upload_to.strip('/'),
        })
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
