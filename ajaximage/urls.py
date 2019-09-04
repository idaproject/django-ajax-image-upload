from django.conf.urls import url

from .views import ajaximage

urlpatterns = [
    url(
        r'^upload/(?P<upload_to>.*)/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<crop>\d+)/(?P<storage>[\w\-.]+)?/',
        ajaximage,
        name='ajaximage',
    )
]
