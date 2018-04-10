from django.contrib.contenttypes.admin import GenericTabularInline

from adminsortable.admin import SortableGenericTabularInline, NonSortableParentAdmin


class ImageInline(SortableGenericTabularInline, GenericTabularInline):
    model = None
    extra = 0




class AjaxImageUploadMixin(NonSortableParentAdmin):
    change_form_template = 'ajaximage/change_form.html'
    ajax_change_form_template_extends = 'adminsortable/change_form.html'

    # noinspection PyProtectedMember
    def change_view(self, request, object_id, form_url='', extra_context=None):

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
        })
        extra_context.update({
            'app_model': f'{self.image_inline.model._meta.app_label}-'
                         f'{self.image_inline.model.__name__.lower()}',
        })
        return super().change_view(request, object_id, form_url='',
                                   extra_context=extra_context)

    # noinspection PyProtectedMember
    def add_view(self, request, form_url='', extra_context=None):

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
        })
        extra_context.update({
            'app_model': f'{self.image_inline.model._meta.app_label}-'
                         f'{self.image_inline.model.__name__.lower()}',
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
