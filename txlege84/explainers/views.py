from django.views.generic import ListView

from explainers.models import Explainer


class ExplainerListDetail(ListView):
    model = Explainer
    template_name = 'pages/explainer-landing.html'
