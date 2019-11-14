import pycountry

from selia_templates.widgets.map_widgets import IrekuaMapWidget
from selia_templates.widgets.map_widgets import IrekuaMapWidgetNoControls


def get_country_name(value):
    return pycountry.countries.lookup(value).name


def site_map(site, type='full'):
    name = 'point_{}'.format(site.pk)
    if type == 'full':
        widget = IrekuaMapWidget(attrs={
            'map_width': '100%',
            'map_height': '100%',
            'id': name,
            'disabled': True})
    else:
        widget = IrekuaMapWidgetNoControls(attrs={
            'map_width': '100%',
            'map_height': '100%',
            'id': name,
            'disabled': True})

    return widget.render(name, site.geo_ref)
