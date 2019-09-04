import os
import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import get_storage_class
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import FileForm
from .image import resize


UPLOAD_PATH = getattr(settings, 'AJAXIMAGE_DIR', 'ajaximage/')
AUTH_TEST = getattr(settings, 'AJAXIMAGE_AUTH_TEST', lambda u: u.is_staff)
FILENAME_NORMALIZER = getattr(settings, 'AJAXIMAGE_FILENAME_NORMALIZER', slugify)


@require_POST
@user_passes_test(AUTH_TEST)
def ajaximage(
    request,
    upload_to=None,
    max_width=0,
    max_height=0,
    crop=0,
    storage=None,
    form_class=FileForm,
):
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        file_ = form.cleaned_data['file']
        image_types = [
            'image/png',
            'image/jpg',
            'image/jpeg',
            'image/pjpeg',
            'image/gif',
            'image/svg+xml',
        ]
        if file_.content_type not in image_types:
            data = json.dumps({'error': 'Bad image format.'})
            return HttpResponse(data, content_type="application/json", status=403)

        file_ = resize(file_, max_width, max_height, crop)
        file_name, extension = os.path.splitext(file_.name)
        safe_name = '{0}{1}'.format(FILENAME_NORMALIZER(file_name), extension)

        storage_obj = get_storage_class(storage)()

        name = os.path.join(upload_to or UPLOAD_PATH, safe_name)
        path = storage_obj.save(name, file_)
        url = storage_obj.url(path)
        return HttpResponse(
            json.dumps({'url': url, 'filename': path}), content_type="application/json"
        )
    return HttpResponse(status=403)
