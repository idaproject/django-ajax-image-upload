from django.conf.urls import url

from .views import ajaximage

urlpatterns = [
    url('^upload/(?P<upload_to>.*)/', ajaximage, name='ajaximage'),
]
