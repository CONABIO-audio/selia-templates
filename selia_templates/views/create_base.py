from django import forms
from django.http import HttpResponseForbidden
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse


class SeliaCreateView(CreateView, SingleObjectMixin):
    no_permission_template = 'selia_templates/generic/no_permission.html'
    success_url = 'selia:home'

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get_success_url_args(self):
        return []

    def get_chain(self):
        return self.request.session.get('chain', '')

    def get_new_chain(self):
        chain = self.get_chain()

        if not chain:
            return ''

        chain_arr = chain.split('|')
        chain_arr.pop(-1)
        self.request.session['chain'] = '|'.join(chain_arr)

        try:
            return chain_arr.pop(-1)
        except:
            return ''

    def get_back_url(self):
        if 'back' in self.request.GET:
            chain_str = self.get_chain()
            return self.request.GET['back']+"?&chain="+chain_str

        return ''

        next_url = self.get_new_chain()

        if next_url == '':
            return self.get_success_url()

        return next_url+"?&chain="+chain_str

    def get_success_url(self):
        return reverse(self.success_url, args=self.get_success_url_args())

    def get_fields_to_remove_on_sucess(self):
        if hasattr(self, 'fields_to_remove'):
            return self.fields_to_remove

        form_class = self.get_form_class()
        return form_class._meta.fields

    def get_additional_query_on_sucess(self):
        return {}

    def modify_query_on_success(self, query):
        query = query.copy()
        fields_to_remove = self.get_fields_to_remove_on_sucess()

        for field in fields_to_remove:
            try:
                query.pop(field)
            except:
                pass

        query_to_add = self.get_additional_query_on_sucess()
        for key, value in query_to_add.items():
            query[key] = value

        return query

    def get_chain_url(self, next_url):
        url = reverse(next_url)
        query = self.modify_query_on_success(self.request.GET)

        full_url = '{url}?{query}'.format(
            url=url,
            query=query.urlencode())
        return full_url

    def redirect_on_success(self):
        next_url = self.get_new_chain()

        if next_url:
            return redirect(self.get_chain_url(next_url))

        return redirect(self.get_success_url())

    def save_form(self, form):
        created_object = form.save(commit=False)
        created_object.created_by = self.request.user
        created_object.save()
        return created_object

    def form_valid(self, form):
        try:
            self.object = self.save_form(form)
            return self.redirect_on_success()
        except forms.ValidationError as errors:
            for field, error in dict(errors).items():
                try:
                    form.add_error(field, error)
                except:
                    form.add_error(None, '{} ({})'.format(
                        str(error), field))

            return self.form_invalid(form)

    def get_objects(self):
        pass

    def post(self, *args, **kwargs):
        self.get_objects()

        if not self.has_view_permission():
            msg = _('User does not have create permissions')
            return HttpResponseForbidden(msg)

        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.get_objects()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['back'] = self.get_back_url()
        return context
