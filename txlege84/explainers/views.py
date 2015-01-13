from django.views.generic import ListView

from explainers.models import Explainer


class ExplainerListDetail(ListView):
    queryset = Explainer.objects.all().published()
    template_name = 'pages/explainer-landing.html'
