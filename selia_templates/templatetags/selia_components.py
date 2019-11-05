import re
import uuid

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from dal_select2.widgets import Select2WidgetMixin

register = template.Library()


@register.inclusion_tag('selia_templates/list.html', takes_context=True)
def list_component(context, template_name, item_list, empty_message):
    context['template_name'] = template_name
    context['item_list'] = item_list
    context['empty_message'] = empty_message
    return context


@register.inclusion_tag('selia_templates/detail.html', takes_context=True)
def detail_component(context, detail_template, object):
    context['detail_template'] = detail_template
    context['object'] = object
    return context


@register.inclusion_tag('selia_templates/help.html', takes_context=True)
def help_component(context, help_template):
    context['help_template'] = help_template
    return context


@register.inclusion_tag('selia_templates/update.html', takes_context=True)
def update_component(context, update_template, form):
    context['update_template'] = update_template
    context['form'] = form
    return context


@register.inclusion_tag('selia_templates/summary.html', takes_context=True)
def summary_component(context, summary_template, object):
    context['summary_template'] = summary_template
    context['object'] = object
    return context


@register.inclusion_tag('selia_templates/filter.html', takes_context=True)
def filter_component(context, template, forms):
    context['template'] = template
    context['forms'] = forms
    return context


@register.inclusion_tag('selia_templates/delete.html', takes_context=True)
def delete_component(context, object):
    context['object'] = object
    return context


@register.inclusion_tag('selia_templates/viewer.html', takes_context=True)
def viewer_component(context, viewer_template, object):
    context['viewer_template'] = viewer_template
    context['object'] = object
    return context


@register.inclusion_tag('selia_templates/create.html', takes_context=True)
def create_component(context, create_template, form):
    context['create_template'] = create_template
    context['form'] = form
    return context


@register.inclusion_tag('selia_templates/create_wizard.html', takes_context=True)
def create_wizard(context, wizard):
    context['wizard'] = wizard
    return context


@register.inclusion_tag('selia_templates/annotator.html', takes_context=True)
def annotator_component(context, annotator_template, item, annotation_list, mode):
    context['annotator_template'] = annotator_template
    context['annotation_list'] = annotation_list
    context['item'] = item
    context['mode'] = mode
    return context


@register.simple_tag
def autocomplete_media():
    extra_script = r'''
    <script>
      $(document).on('click', '.dropdown-menu .select2*', function(e) {
        e.stopPropagation();
      });
    </script>
    '''

    media = '''
    {select2_media}
    {extra_script}
    '''.format(
        select2_media=Select2WidgetMixin().media,
        extra_script=extra_script)

    return mark_safe(media)


@register.inclusion_tag('selia_templates/filter_bar.html', takes_context=True)
def filter_bar(context, forms):
    context['forms'] = forms

    search_form = forms['search']
    search_field = search_form.fields['search']
    search_field = search_field.get_bound_field(search_form, 'search')

    if search_field.data:
        context['search'] = search_field.data
        context['clear'] = True

    context['form'] = {}
    filter_form = forms['filter']
    for field_name, field in filter_form._form.fields.items():
        bound_field = field.get_bound_field(filter_form._form, field_name)
        if bound_field.data:
            context['form'][field_name] = {
                'data': bound_field.data,
                'label': field.label
            }
            context['clear'] = True

    return context


@register.filter(name='remove_option')
def remove_option(value, field):
    regex = r'({}=)([^&]+)'.format(field)
    result = re.sub(regex, r'\1', value)
    return result


FORM_ICONS = {
    'exact': '<i class="fas fa-equals"></i>',
    'iexact':'<i class="fas fa-equals"></i>',
    'in': '<i class="fas fa-list-ol"></i>',
    'lt': '<i class="fas fa-less-than"></i>',
    'gt': '<i class="fas fa-greater-than"></i>',
    'gte': '<i class="fas fa-greater-than-equal"></i>',
    'lte': '<i class="fas fa-less-than-equal"></i>',
    'icontains': '<i class="fas fa-font"></i>',
    'contains': '<i class="fas fa-font"></i>',
    'istartswith': '<i class="fas fa-font"></i>',
    'startswith': '<i class="fas fa-font"></i>',
    'iendswith': '<i class="fas fa-font"></i>',
    'endswith': '<i class="fas fa-font"></i>',
    'regex': '<i class="fas fa-terminal"></i>',
    'iregex': '<i class="fas fa-terminal"></i>',
}


@register.filter(name='selia_form', is_safe=True)
def selia_form(form, label):
    widget = form.field.widget

    custom_attrs = ' form-control'
    if widget.input_type == 'select':
        custom_attrs += ' custom-select'

    if widget.input_type == 'file':
        custom_attrs = 'custom-file-input'

    widget_attrs = widget.attrs.get('class', '')
    class_for_html = widget_attrs + custom_attrs

    input_html = form.as_widget(attrs={'class': class_for_html})

    try:
        lookup_expr = form.html_name.split('__')[-1]
        icon = FORM_ICONS.get(lookup_expr, FORM_ICONS['exact'])
    except:
        icon = FORM_ICONS['exact']

    prepend_html = '''
    <div class="input-group-prepend">
        <span class="input-group-text" id="{prepend_id}">
            {prepend_icon}
        </span>
    </div>
    '''.format(
        prepend_id=form.html_name + '_prepend',
        prepend_icon=icon
    )

    append_html = '''
    <div class="input-group-append">
        <button type="submit" class="btn btn-outline-success" type="button" id="{append_id}">
            {append_icon} <i class="fas fa-plus"></i>
        </button>
    </div>
    '''.format(
        append_id=form.html_name + '_append',
        append_icon=_('add')
    )

    help_text_html = '''
    <small id="{help_text_id}" class="form-text text-muted">{help_text}</small>
    '''.format(
        help_text_id=form.html_name + '_help_text',
        help_text=form.help_text
    )

    if label:
        label_html = form.label_tag(contents=label)
    elif label is None:
        label_html = ''
    else:
        label_html = form.label_tag()

    form_html = '''
      <div class="form-group w-100">
        <small>{label_html}</small>
        <div class="input-group">
            {prepend_html}
            {input_html}
            {append_html}
        </div>
        {help_text_html}
      </div>
    '''
    form_html = form_html.format(
        label_html=label_html,
        prepend_html=prepend_html,
        input_html=input_html,
        append_html=append_html,
        help_text_html=help_text_html
    )

    return mark_safe(form_html)


@register.inclusion_tag('selia_templates/bootstrap_form.html')
def bootstrap_form(form):
    return {'form': form}


@register.filter(name='update_metadata', is_safe=True)
def update_metadata(form, metadata):
    form.update_metadata(metadata)


@register.filter(name='remove_fields', is_safe=True)
def remove_fields(query, fields):
    fields = fields.split('&')
    query = query.copy()

    for field in fields:
        try:
            query.pop(field)
        except KeyError:
            pass

    return query.urlencode()


@register.filter(name='add_chain', is_safe=True)
def add_chain(query, view_name):
    query_copy = query.copy()
    query_copy['chain'] = '{previous}|{new}'.format(
        previous=query.get('chain', ''),
        new=view_name)
    return query_copy.urlencode()


@register.filter(name='add_fields', is_safe=True)
def add_fields(query, fields):
    query_copy = query.copy()
    try:
        fields = fields.split('&')
    except:
        return query_copy.urlencode()

    for field in fields:
        try:
            key, value = field.split("=")
            query_copy[key] = value
        except:
            pass

    return query_copy.urlencode()


@register.simple_tag
def remove_form_fields(query, forms):
    query = query.copy()

    if 'filter' in forms:
        filter_form = forms['filter']
        filter_prefix = filter_form._form.prefix
        for field in filter_form._form.fields:
            if filter_prefix:
                field = '{}-{}'.format(filter_prefix, field)
            try:
                query.pop(field)
            except:
                pass

    if 'search' in forms:
        search_form = forms['search']
        search_prefix = search_form.prefix
        for field in search_form.fields:
            if search_prefix:
                field = '{}-{}'.format(search_prefix, field)
            try:
                query.pop(field)
            except:
                pass

    if 'order' in forms:
        order_form = forms['order']
        order_prefix = order_form.prefix
        for field in order_form.fields:
            if order_prefix:
                field = '{}-{}'.format(order_prefix, field)
            try:
                query.pop(field)
            except:
                pass

    return query.urlencode()


@register.inclusion_tag('selia_templates/selected_item.html')
def selected_item(template, item, label):
    random_id = uuid.uuid4().hex.lower()[0:8]
    full_template_name = 'selia_templates/select_list_items/{name}.html'
    return {
        'template': full_template_name.format(name=template),
        'item': item,
        'id': random_id,
        'label': label
    }


@register.inclusion_tag('selia_templates/is_own_checkbox.html')
def is_own_checkbox(form):
    return {'form': form}
