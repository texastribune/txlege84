from django.views.generic import DetailView

from bills.mixins import AllSubjectsMixin
from legislators.models import Legislator


class LegislatorDetail(AllSubjectsMixin, DetailView):
    model = Legislator
    template_name = 'pages/legislator.html'
