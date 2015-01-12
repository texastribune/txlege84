from django.views.generic import DetailView, ListView

from bills.mixins import AllSubjectsMixin
from bills.models import Bill, Subject


class BillDetail(AllSubjectsMixin, DetailView):
    model = Bill
    template_name = 'pages/bill.html'


class SubjectDetail(AllSubjectsMixin, DetailView):
    model = Subject
    template_name = 'pages/subject.html'


class LegeStreamDetail(AllSubjectsMixin, ListView):
    model = Bill
    template_name = 'pages/legestream.html'

