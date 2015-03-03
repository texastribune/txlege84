from django.views.generic import ListView

from core.mixins import ConveneTimeMixin

from explainers.models import Explainer


class ExplainerListDetail(ConveneTimeMixin, ListView):
    queryset = Explainer.objects.all().published()
    template_name = 'pages/explainer-landing.html'
