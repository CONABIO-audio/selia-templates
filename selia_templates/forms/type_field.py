from django import forms
from selia_templates.widgets.type_select_widget import TypeSelectWidget


class TypeSelectField(forms.ModelChoiceField):
    widget = TypeSelectWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_label = None
        self.initial = self.queryset.first()

    def label_from_instance(self, obj):
        return obj
