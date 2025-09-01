from django import template

register = template.Library()

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={**field.field.widget.attrs, "class": css})
