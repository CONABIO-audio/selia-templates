from django import forms
from django.views.generic import ListView
from django.utils.translation import gettext as _
from django.shortcuts import render

from selia_templates.views.search_filter import SearchFilter


class SearchForm(forms.Form):
    search = forms.CharField(
        label=_('search'),
        max_length=100,
        required=False)


class SeliaListView(ListView):
    paginate_by = 10
    empty_message = _('Empty list')
    no_permission_template = 'selia_templates/generic/no_permission.html'

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def has_create_permission(self):
        return True

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def clean_chain(self):
        self.request.session['chain'] = ''

    def get(self, *args, **kwargs):
        self.clean_chain()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)

    def get_list_item_template(self):
        if hasattr(self, 'list_item_template'):
            return self.list_item_template

        return NotImplementedError('No template for list item was given')

    def get_filter_form_template(self):
        if hasattr(self, 'filter_form_template'):
            return self.filter_form_template

        return NotImplementedError('No template for filter form was given')

    def get_help_template(self):
        if hasattr(self, 'help_template'):
            return self.help_template

        raise NotImplementedError('No template for help was given')

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_ordering_choices(self):
        orderings = []
        for field, label in self.ordering_fields:
            orderings.append(
                (
                    '-{field}'.format(field=field),
                    '{order} {label}'.format(
                        label=label, order=_('↓'))
                )
            )

            orderings.append(
                (
                    field,
                    '{order} {label}'.format(
                        label=label, order=_('↑'))
                )
            )
        return orderings

    def get_ordering_form(self):
        ordering_choices = self.get_ordering_choices()

        class OrderingForm(forms.Form):
            order = forms.ChoiceField(
                label=_('ordering'),
                choices=ordering_choices)

        ordering_form = OrderingForm(self.request.GET)
        return ordering_form

    def get_filter_class(self):
        if hasattr(self, 'filter_class'):
            return self.filter_class

        raise NotImplementedError('No filter class was provided')

    def get_initial_queryset(self):
        if hasattr(self, 'queryset'):
            return self.queryset

        raise NotImplementedError('No initial queryset was provided')

    def get_queryset(self):
        queryset = self.get_initial_queryset()
        return self.filter_queryset(queryset)

    def filter_queryset_with_query(self, queryset):
        try:
            filter_class = self.get_filter_class()
            self.filter = filter_class(
                self.request.GET,
                queryset=queryset,
                request=self.request)
            queryset = self.filter.qs
        except NotImplementedError:
            pass

        return queryset

    def filter_queryset_with_search(self, queryset):
        if hasattr(self, 'search_fields'):
            self.search_form = self.get_search_form()

            if self.search_form.is_valid():
                queryset = SearchFilter().filter_queryset(self.request, queryset, self)

        return queryset

    def order_queryset(self, queryset):
        if hasattr(self, 'ordering_fields'):
            self.order_form = self.get_ordering_form()

            if self.order_form.is_valid():
                ordering = self.order_form.data['order']
                queryset = queryset.order_by(ordering)

        return queryset

    def filter_queryset(self, queryset):
        queryset = self.filter_queryset_with_query(queryset)
        queryset = self.filter_queryset_with_search(queryset)
        return self.order_queryset(queryset)

    def get_permissions(self):
        return {
            'create': self.has_create_permission()
        }

    def get_templates(self):
        return {
            'help': self.get_help_template(),
            'list_item': self.get_list_item_template(),
            'filter_form': self.get_filter_form_template(),
        }

    def get_forms(self):
        forms = {}
        if hasattr(self, 'filter'):
            forms['filter'] = self.filter

        if hasattr(self, 'search_form'):
            forms['search'] = self.search_form

        if hasattr(self, 'order_form'):
            forms['order'] = self.order_form

        return forms

    def get_context_data(self, **kwargs):
        context = {'object_list': super().get_context_data(**kwargs)}
        context['forms'] = self.get_forms()
        context['templates'] = self.get_templates()
        context['permissions'] = self.get_permissions()
        return context
