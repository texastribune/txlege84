# from django.shortcuts import render
from django.views.generic import DetailView

from committees.models import Committee


class CommitteeDetail(DetailView):
    model = Committee
    template_name = 'committee.html'

# Create your views here.
