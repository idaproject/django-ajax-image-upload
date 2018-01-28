from django.core.files.storage import default_storage
from django.db.models.fields.files import FileDescriptor, FieldFile
from django.db.models import Field
from .widgets import AjaxImageWidget


class AjaxImageField(Field):

    storage = default_storage
    attr_class = FieldFile
    descriptor_class = FileDescriptor

    def __init__(self, *args, **kwargs):
        upload_to = kwargs.pop('upload_to', '')
        self.widget = AjaxImageWidget(upload_to=upload_to)
        super(AjaxImageField, self).__init__(*args, **kwargs)

    # noinspection PyMethodOverriding
    def contribute_to_class(self, cls, name, virtual_only=False):
        super(AjaxImageField, self).contribute_to_class(cls, name, virtual_only)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_prep_value(self, value):
        if value is None:
            return None
        return str(value)

    def get_internal_type(self):
        return 'TextField'

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(AjaxImageField, self).formfield(**defaults)
