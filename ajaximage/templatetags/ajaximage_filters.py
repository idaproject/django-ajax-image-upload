from django import template

register = template.Library()


@register.filter(name='upload_to')
def upload_to(model):
    fields = model._meta.get_fields()
    field = next((field for field in fields if hasattr(field, 'upload_to')), None)
    if not field:
        return None
    if callable(field.upload_to):
        return field.upload_to(model, '').strip('/')
    return field.upload_to

