from abc import abstractmethod
from django.views import View

from django.shortcuts import reverse
from django.shortcuts import render
from django.shortcuts import redirect


class MissingParameterError(Exception):
    """Missing GET parameter in request"""


class CreateManagerBase(View):
    no_permission_template = 'selia_templates/generic/no_permission.html'
    required_get_parameters = []
    manager_name = 'base_manager'

    def check_get_parameters(self):
        for param in self.required_get_parameters:
            if param not in self.request.GET:
                raise MissingParameterError(param)

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    @abstractmethod
    def view_from_request(self):
        pass

    def get_redirect_url(self):
        view_name = self.view_from_request()
        url = reverse(view_name)
        final_url = '{url}?{query}'.format(
            url=url,
            query=self.request.GET.urlencode())
        return final_url

    def check_chain(self):
        session = self.request.session
        chain = session.get('chain', '').split('|')

        if not self.manager_name == chain[-1]:
            chain.append(self.manager_name)
            session['chain'] = '|'.join(chain)

    def get(self, request):
        self.request = request
        self.check_chain()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        try:
            self.check_get_parameters()
        except MissingParameterError:
            return self.no_permission_redirect()

        url = self.get_redirect_url()
        return redirect(url)
