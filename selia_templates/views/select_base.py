from django.views.generic import TemplateView
from django.shortcuts import render


class SeliaSelectView(TemplateView):
    no_permission_template = 'selia_templates/generic/no_permission.html'
    prefix = ''
    create_url = ''

    def get_list_class(self):
        if hasattr(self, 'list_class'):
            return self.list_class

        msg = 'User did not supply a list class or overwrite get list class method'
        raise NotImplementedError(msg)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['list'] = self.get_list_context_data()
        context['prefix'] = self.prefix
        context['create_url'] = self.create_url
        return context

    def get_list_context_data(self):
        list_class = self.get_list_class()

        if not list_class.prefix:
            list_class.prefix = self.prefix

        list_instance = list_class(self.request)
        return list_instance.get_context_data()

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get_objects(self):
        pass

    def get(self, *args, **kwargs):
        self.get_objects()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)
