from django.contrib.gis import forms


class IrekuaMapWidget(forms.OSMWidget):
    default_zoom = 12
    template_name = 'selia_templates/widgets/map_widget.html'


class IrekuaMapWidgetNoControls(forms.OSMWidget):
    default_zoom = 9
    template_name = 'selia_templates/widgets/map_widget_no_controls.html'


class IrekuaMapWidgetObscured(forms.OSMWidget):
    default_zoom = 12
    template_name = 'selia_templates/widgets/map_widget_obscured.html'
