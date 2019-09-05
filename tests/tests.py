import json
import os

from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.admin.sites import AdminSite

from .models import Gallery, Image
from ajaximage.admin import AjaxImageUploadMixin
from ajaximage.fields import AjaxImageField
from ajaximage.widgets import AjaxImageWidget


class MockRequest:
    method = 'post'


class MockSuperUser:
    def has_perm(self, perm):
        return True


class MockStorage:
    def save(self, name, file):
        return 'test/path'

    def url(self, path):
        return 'test/url'


request = MockRequest()
request.user = MockSuperUser()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class AjaxImageUploadMixinTest(TestCase):
    def setUp(self):
        self.gallery = Gallery.objects.create(name='Test gallery')
        self.site = AdminSite()
        self.client = Client()
        self.user = User.objects.create_superuser('test_user', '', '')

    def test_change_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin:tests_gallery_change', args=(self.gallery.pk,)))
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)

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
                        'storage': '',
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
        with open(os.path.join(BASE_PATH, 'test.jpg'), 'rb') as f:
            response = self.client.post(
                reverse(
                    'ajaximage',
                    kwargs={
                        'upload_to': 'test/folder',
                        'max_width': 300,
                        'max_height': 300,
                        'crop': 0,
                        'storage': 'tests.tests.MockStorage',
                    },
                ),
                {'file': f},
            )
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {'url': 'test/url', 'filename': 'test/path'})

        with open(os.path.join(BASE_PATH, 'test.jpg'), 'rb') as f:
            response = self.client.post(
                reverse(
                    'ajaximage',
                    kwargs={
                        'upload_to': 'test/folder',
                        'max_width': 300,
                        'max_height': 300,
                        'crop': 0,
                        'storage': '',
                    },
                ),
                {'file': f},
            )
            self.assertEqual(response.status_code, 200)


class AjaxImageFieldTest(TestCase):
    def test_widget_render(self):
        self.maxDiff = None
        file_path = os.path.join(BASE_PATH, 'test.jpg')
        file_url = MockStorage().url(file_path)
        field = AjaxImageField(
            upload_to='test', max_width=100, max_height=200, storage_path='tests.tests.MockStorage'
        )
        html = field.widget.render(name='test', value=file_path, attrs={'id': 1})
        correct_html = AjaxImageWidget.html.format(
            file_path=file_path,
            file_url=file_url,
            element_id=1,
            name='test',
            upload_url='/ajaximage/upload/test/100/200/0/tests.tests.MockStorage/',
        )
        self.assertHTMLEqual(html, correct_html)
