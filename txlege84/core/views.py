from django.views.generic import ListView

from bills.mixins import AllSubjectsMixin
from core.mixins import ConveneTimeMixin
from legislators.mixins import AllLegislatorsMixin, ChambersMixin

from explainers.models import Explainer
from topics.models import Topic


class LandingView(AllSubjectsMixin, AllLegislatorsMixin,
                  ChambersMixin, ConveneTimeMixin, ListView):
    model = Topic
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['explainer_list'] = Explainer.objects.all().published()

        return context
