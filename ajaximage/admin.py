from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.fields import ReverseGenericManyToOneDescriptor
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor

from adminsortable.admin import SortableGenericTabularInline, NonSortableParentAdmin


class ImageInline(SortableGenericTabularInline, GenericTabularInline):
    model = None
    extra = 0


class AjaxImageUploadMixin(NonSortableParentAdmin):
    change_form_template = 'ajaximage/change_form.html'
    ajax_change_form_template_extends = 'adminsortable/change_form.html'
    image_inline = ImageInline
    upload_to = '/images/'
    images_field = None

    # noinspection PyProtectedMember
    def change_view(self, request, object_id, form_url='', extra_context=None):

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'ajax_change_form_template_extends': self.ajax_change_form_template_extends,
        })
        images_field = getattr(self.model, self.images_field)
        row_class = None
        if isinstance(images_field, ReverseGenericManyToOneDescriptor):
            app_label = images_field.rel.model._meta.app_label
            model_name = images_field.rel.model.__name__.lower()
            row_class = 'dynamic-{}-{}-content_type-object_id'.format(app_label, model_name)
        elif isinstance(images_field, ReverseManyToOneDescriptor):
            row_class = 'dynamic-{}'.format(self.images_field)
        extra_context.update({
            'upload_to': reverse('ajaximage', kwargs={'upload_to': self.upload_to.strip('/')}),
            'row_class': row_class,
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
        images_field = getattr(self.model, self.images_field)
        row_class = None
        if isinstance(images_field, ReverseGenericManyToOneDescriptor):
            app_label = images_field.rel.model._meta.app_label
            model_name = images_field.rel.model.__name__.lower()
            row_class = 'dynamic-{}-{}-content_type-object_id'.format(app_label, model_name)
        elif isinstance(images_field, ReverseManyToOneDescriptor):
            row_class = 'dynamic-{}'.format(self.images_field)
        extra_context.update({
            'upload_to': reverse('ajaximage', kwargs={'upload_to': self.upload_to.strip('/')}),
            'row_class': row_class
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
