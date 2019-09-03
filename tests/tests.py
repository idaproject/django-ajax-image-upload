import json

from django.contrib.admin import ModelAdmin, TabularInline
from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.sites import AdminSite

from .models import Gallery, Image
from ajaximage.admin import AjaxImageUploadMixin


class MockRequest:
    method = 'post'


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class AjaxImageUploadMixinTest(TestCase):
    def setUp(self):
        self.gallery = Gallery.objects.create(name='Test gallery')
        self.site = AdminSite()

    def test_context_upload_to(self):
        class ImageInline(TabularInline):
            model = Image
            ajax_image_upload_field = 'file'

        class CustomViewImageInline(TabularInline):
            model = Image
            ajax_image_upload_field = 'file'
            ajax_image_upload_url = '/different-url/'

        class GalleryAdmin(AjaxImageUploadMixin, ModelAdmin):
            inlines = (ImageInline, CustomViewImageInline)

        ma = GalleryAdmin(Gallery, self.site)
        data = json.loads(ma._get_context(request, self.gallery.pk, None)['data'])
        upload_to_urls = [el['upload_to'] for el in data]
        self.assertEqual(
            upload_to_urls,
            [reverse('ajaximage', kwargs={'upload_to': 'test/folder'}), '/different-url/'],
        )
