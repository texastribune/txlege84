from django.views.generic import ListView, DetailView

from bills.mixins import AllSubjectsMixin
from core.mixins import ConveneTimeMixin
from legislators.mixins import AllLegislatorsMixin
from legislators.models import Legislator

class LegislatorList(AllLegislatorsMixin, ConveneTimeMixin, ListView):
    model = Legislator
    template_name = 'pages/legislator-landing.html'

class LegislatorDetail(AllSubjectsMixin, AllLegislatorsMixin,
                       ConveneTimeMixin, DetailView):
    model = Legislator
    template_name = 'pages/legislator.html'
