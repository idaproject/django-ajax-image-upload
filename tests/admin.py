from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Gallery, Image
from ajaximage.admin import AjaxImageUploadMixin


class ParameterImageInline(TabularInline):
    model = Image
    ajax_image_upload_field = 'file'
    ajax_image_max_width = 500
    ajax_image_max_height = 500
    ajax_image_crop = 1
    ajax_image_storage_path = 'test.path'


@admin.register(Gallery)
class GalleryAdmin(AjaxImageUploadMixin, admin.ModelAdmin):
    inlines = (ParameterImageInline,)
