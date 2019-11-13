from django import template
from django.template.loader import get_template

from selia_templates.widgets.map_widgets import IrekuaMapWidget
from selia_templates.widgets.map_widgets import IrekuaMapWidgetNoControls


register = template.Library()


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


@register.inclusion_tag('selia_templates/list/list_icon.html')
def list_icon(item, size='5em'):
    return {'item': item, 'size':size}


@register.inclusion_tag('selia_templates/detail/detail_icon.html')
def detail_icon(item):
    return {'item': item}


@register.tag
def listattribute(parser, token):
    header = parser.parse(('attributevalue',))
    parser.delete_first_token()

    content = parser.parse(('endlistattribute'))
    parser.delete_first_token()
    return GenericNode(
        template_name='selia_templates/list/list_attribute.html',
        header=header,
        content=content)


@register.tag
def listtitle(parser, token):
    try:
        image = parser.parse(('endlistimage',))
        parser.delete_first_token()
    except:
        image = None

    title = parser.parse(('endlistheader', ))
    parser.delete_first_token()

    try:
        description = parser.parse(('endlisttitle', ))
        parser.delete_first_token()
    except:
        description = None

    return GenericNode(
        template_name='selia_templates/list/list_item_title.html',
        title=title,
        image=image,
        description=description)

@register.tag
def listsummary(parser, token):
    title = parser.parse(('summarycount',))
    parser.delete_first_token()

    count = parser.parse(('summarybuttons', 'endlistsummary'))
    tag = parser.next_token()

    buttons = None
    if tag.contents == 'summarybuttons':
        buttons = parser.parse(('endlistsummary', ))
        parser.delete_first_token()

    return GenericNode(
        template_name='selia_templates/list/list_item_summary.html',
        title=title,
        count=count,
        buttons=buttons)


@register.tag
def detailitem(parser, token):
    header = parser.parse(('endhead',))
    parser.delete_first_token()

    content = parser.parse(('enddetailitem'))
    parser.delete_first_token()
    return GenericNode(
        template_name='selia_templates/detail/detail_item.html',
        header=header,
        content=content)


@register.tag
def detailtitle(parser, token):
    try:
        image = parser.parse(('enddetailimage',))
        parser.delete_first_token()
    except:
        image = None

    title = parser.parse(('enddetailheader', ))
    parser.delete_first_token()

    try:
        description = parser.parse(('enddetailtitle', ))
        parser.delete_first_token()
    except:
        description = None

    return GenericNode(
        template_name='selia_templates/detail/detail_title.html',
        title=title,
        image=image,
        description=description)


@register.tag
def detailsection(parser, token):
    content = parser.parse(('enddetailsection',))
    parser.delete_first_token()
    return GenericNode(
        template_name='selia_templates/detail/detail_section.html',
        content=content)


@register.filter(name='site_map')
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


@register.filter(name='is_not_trivial_schema')
def is_not_trivial_schema(schema):
    return len(schema['required']) != 0
