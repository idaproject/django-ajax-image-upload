from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import AjaxImageField


# noinspection PyAbstractClass
class AbstractImage(models.Model):
    order = models.PositiveIntegerField('Порядок', default=0, editable=False, db_index=True)
    file = AjaxImageField('Файл', upload_to='ajaximage/image/file')
    description = models.TextField('Описание', blank=True)

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey()

    class Meta:
        abstract = True
        ordering = ['order']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return str(self.order)
