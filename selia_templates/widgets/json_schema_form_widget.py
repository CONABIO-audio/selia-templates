import json
from django.forms.widgets import Widget


class JsonSchemaFormWidget(Widget):
    template_name = 'selia_templates/widgets/json_form_widget.html'
    input_type = 'text'

    class Media:
        js = ('selia_templates/js/selia_json_form.js', )

    def format_value(self, value):
        try:
            value = json.dumps(value)
        except TypeError:
            value = json.dumps({})
        return value
