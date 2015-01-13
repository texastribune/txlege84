from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

from bills.mixins import AllSubjectsMixin
from legislators.mixins import AllLegislatorsMixin
from bills.models import Bill, Subject


class BillDetail(AllSubjectsMixin, AllLegislatorsMixin, DetailView):
    model = Bill
    template_name = 'pages/bill.html'


class SubjectDetail(AllSubjectsMixin, AllLegislatorsMixin, DetailView):
    model = Subject
    template_name = 'pages/subject.html'


class BillSearchJson(ListView):
    queryset = Bill.objects.all().values('name', 'slug')

    def render_to_response(self, context, **kwargs):
        return JsonResponse(list(context['object_list']), safe=False)


class LegeStreamDetail(AllSubjectsMixin, AllLegislatorsMixin, TemplateView):
    template_name = 'pages/legestream.html'
