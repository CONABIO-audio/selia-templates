from django import template

register = template.Library()


@register.inclusion_tag('selia_templates/buttons/help.html')
def help_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/see.html')
def see_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/enter.html')
def enter_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/add.html')
def add_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/update.html')
def update_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/edit.html')
def edit_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/add_user.html')
def add_user_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/remove_user.html')
def remove_user_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/email.html')
def email_button():
    return {}


@register.inclusion_tag('selia_templates/buttons/back.html')
def back_button(next):
    return {'next': next}
