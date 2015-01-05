from django.views.generic import DetailView

from bills.mixins import AllSubjectsMixin
from bills.models import Bill, Subject


class BillDetail(AllSubjectsMixin, DetailView):
    model = Bill
    template_name = 'pages/bill.html'


class SubjectDetail(DetailView):
    model = Subject
    template_name = 'pages/subject.html'
