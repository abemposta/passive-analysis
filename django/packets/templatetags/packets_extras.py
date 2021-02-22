from django import template

register = template.Library()

@register.filter(name='fields')
def fields(value, key):
    if key in value:
        return value[key]
    else:
        return None


@register.simple_tag
def template_exists(template_name):
    try:
        template.loader.get_template(template_name)
        return "Template exists"
    except template.TemplateDoesNotExist:
        return "Template doesn't exist"

@register.filter(name='thead')
def thead(strfields):
    fields = strfields
    thead = ""
    for field in fields:
        thead += "<th>" + field + "</th> \n"
    return thead

