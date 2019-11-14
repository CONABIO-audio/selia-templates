from django import template
from django.template.loader import get_template


class GenericNode(template.Node):
    def __init__(self, template_name=None, **kwargs):
        self.template_name = template_name
        self.kwargs = kwargs

    def render(self, context):
        template = get_template(self.template_name)
        template_context = {
            key: value.render(context)
            for key, value in self.kwargs.items()
            if value is not None
        }
        return template.render(template_context)
