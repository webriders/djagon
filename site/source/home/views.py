from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'home/home_page.html'

    def get_context_data(self, **kwargs):
        data = super(HomePageView, self).get_context_data(**kwargs)
        return data


home_page = HomePageView.as_view()
