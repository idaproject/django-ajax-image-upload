from django import template

register = template.Library()


@register.filter(name='upload_to')
def upload_to(model):
    fields = model._meta.get_fields()
    return next((field.upload_to for field in fields if hasattr(field, 'upload_to')), None)
