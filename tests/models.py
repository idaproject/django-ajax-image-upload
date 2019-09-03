from django.db import models

from ajaximage.fields import AjaxImageField


class Gallery(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=100)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    file = AjaxImageField(upload_to='test/folder')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

