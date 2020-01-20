from django.template import Node
from django.template.loader import get_template


class GenericNode(Node):
    def __init__(self, template_name=None, **kwargs):
        self.template_name = template_name
        self.data = kwargs

    def render(self, context):
        template = get_template(self.template_name)
        template_context = {
            key: value.render(context)
            for key, value in self.data.items()
            if value is not None
        }

        return template.render(template_context)


class ComplexNode(Node):
    child_nodelists = ('nodelist', 'brand', 'items', )

    def __init__(self, template_name=None, brand=None, items=None):
        self.template_name = template_name
        self.brand = brand
        self.items = items

    def render(self, context):
        template = get_template(self.template_name)

        print('brand', self.brand)
        print('items', self.items)

        template_context = {
            "brand": self.brand.render(context),
            "items": self.items.render(context),
        }

        return template.render(template_context)
