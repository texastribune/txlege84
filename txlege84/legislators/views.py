from django.views.generic import DetailView

from bills.mixins import AllSubjectsMixin
from legislators.mixins import AllLegislatorsMixin
from legislators.models import Legislator


class LegislatorDetail(AllSubjectsMixin, AllLegislatorsMixin, DetailView):
    model = Legislator
    template_name = 'pages/legislator.html'
