from django import forms


class TypeSelectWidget(forms.RadioSelect):
    template_name = 'selia_templates/widgets/type_input.html'
    option_template_name = 'selia_templates/widgets/type_option.html'
