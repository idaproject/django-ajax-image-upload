from django.conf.urls import url

urlpatterns = [
    url('^upload/(?P<upload_to>.*)/', 'ajaximage.views.ajaximage', name='ajaximage'),
]
