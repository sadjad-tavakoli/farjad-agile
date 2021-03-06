from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('members:self:books:all'))
        return redirect(reverse('members:authentication:phone'))
