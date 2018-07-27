from django import template

register = template.Library()


@register.filter(name='upload_to')
def upload_to(model):
    fields = model._meta.get_fields()
    field = next((field for field in fields if hasattr(field, 'upload_to')), None)
    if callable(field.upload_to):
        return field.upload_to(model, '')
    return field.upload_to

