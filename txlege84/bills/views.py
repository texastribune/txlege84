from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

from bills.mixins import AllSubjectsMixin
from committees.mixins import AllCommitteesMixin
from legislators.mixins import AllLegislatorsMixin, ChambersMixin
from bills.models import Bill, Subject


class BillDetail(AllSubjectsMixin, AllLegislatorsMixin, DetailView):
    model = Bill
    template_name = 'pages/bill.html'


class SubjectDetail(AllSubjectsMixin, AllLegislatorsMixin, DetailView):
    model = Subject
    template_name = 'pages/subject.html'


class SubjectListDetail(ListView):
    model = Subject
    template_name = 'pages/subject-list.html'


class BillSearchView(AllLegislatorsMixin, AllSubjectsMixin,
                     AllCommitteesMixin, TemplateView):
    template_name = 'pages/find-bills.html'


class BillSearchJson(ListView):
    queryset = Bill.objects.all().values('name', 'slug')

    def render_to_response(self, context, **kwargs):
        return JsonResponse(list(context['object_list']), safe=False)


class LegeStreamDetail(AllSubjectsMixin, AllLegislatorsMixin,
                       ChambersMixin, TemplateView):
    template_name = 'pages/legestream.html'
