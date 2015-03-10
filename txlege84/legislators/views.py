from django.views.generic import DetailView

from bills.mixins import AllSubjectsMixin
from core.mixins import ConveneTimeMixin
from legislators.mixins import AllLegislatorsMixin
from legislators.models import Legislator


class LegislatorDetail(AllSubjectsMixin, AllLegislatorsMixin,
                       ConveneTimeMixin, DetailView):
    model = Legislator
    template_name = 'pages/legislator.html'
