from django.views.generic import DetailView

from legislators.models import Legislator


class LegislatorDetail(DetailView):
    model = Legislator
    template_name = 'legislator.html'
