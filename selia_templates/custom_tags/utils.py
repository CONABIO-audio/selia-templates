import pycountry
from uuid import uuid4

from selia_templates.widgets.map_widgets import IrekuaMapWidget
from selia_templates.widgets.map_widgets import IrekuaMapWidgetNoControls


def get_country_name(value):
    return pycountry.countries.lookup(value).name


def site_map(site, type='full'):
    name = 'point_{}_{}'.format(site.pk, str(uuid4())[:5])
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


def cut_pagination(range, page=1):
    length = len(range)
    if length < 6:
        return {
            'range': range,
            'pre_ellipsis': False,
            'post_ellipsis': False
        }

    lower_limit = max(0, page - 3)
    upper_limit = min(page + 2, length)

    return {
        'range': range[lower_limit: upper_limit],
        'pre_ellipsis': page > 3,
        'post_ellipsis': length - page > 2
    }
