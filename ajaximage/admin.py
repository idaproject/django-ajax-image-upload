from django.contrib.contenttypes.admin import GenericTabularInline

from adminsortable.admin import SortableGenericTabularInline, NonSortableParentAdmin


class ImageInline(SortableGenericTabularInline, GenericTabularInline):
    model = None
    extra = 0




class AjaxImageUploadMixin(NonSortableParentAdmin):
    change_form_template = 'ajaximage/change_form.html'
    ajax_change_form_template_extends = 'adminsortable/change_form.html'
    image_inline = ImageInline
    inline_position = None

    def add_image_inline(self):
        if not isinstance(self.inline_position, int):
            self.inline_position = len(self.inlines)
        if not isinstance(self.inlines, list):
            self.inlines = list(self.inlines)
        self.inlines.insert(self.inline_position, self.image_inline)

    def get_inline_instances(self, request, obj=None):
        if self.image_inline not in self.inlines:
            self.add_image_inline()
        return super().get_inline_instances(request, obj)

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
