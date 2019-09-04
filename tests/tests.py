import json
import os

from django.contrib.admin import ModelAdmin, TabularInline
from django.test import TestCase, Client
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

    def test_ajaximage_url_parameter(self):
        class ImageInline(TabularInline):
            model = Image
            ajax_image_upload_field = 'file'

        class ParameterImageInline(TabularInline):
            model = Image
            ajax_image_upload_field = 'file'
            ajax_image_max_width = 500
            ajax_image_max_height = 500
            ajax_image_crop = 1
            ajax_image_storage_path = 'test.path'

        class GalleryAdmin(AjaxImageUploadMixin, ModelAdmin):
            inlines = (ImageInline, ParameterImageInline)

        ma = GalleryAdmin(Gallery, self.site)
        data = json.loads(ma._get_context(request, self.gallery.pk, None)['data'])
        url = [el['ajaximage_url'] for el in data]
        self.assertEqual(
            url,
            [
                reverse(
                    'ajaximage',
                    kwargs={
                        'upload_to': 'test/folder',
                        'max_width': 0,
                        'max_height': 0,
                        'crop': 0,
                        'storage': None,
                    },
                ),
                reverse(
                    'ajaximage',
                    kwargs={
                        'upload_to': 'test/folder',
                        'max_width': 500,
                        'max_height': 500,
                        'crop': 1,
                        'storage': 'test.path',
                    },
                ),
            ],
        )


class AjaximageViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_status(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_path, 'test.jpg'), 'rb') as f:
            response = self.client.post(
                reverse(
                    'ajaximage',
                    kwargs={
                        'upload_to': 'test/folder',
                        'max_width': 300,
                        'max_height': 300,
                        'crop': 0,
                        'storage': 'django.core.files.storage.FileSystemStorage',
                    },
                ),
                {'file': f},
            )
            self.assertEqual(response.status_code, 200)
