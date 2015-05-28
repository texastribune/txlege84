from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

from bills.mixins import AllSubjectsMixin
from core.mixins import ConveneTimeMixin
from committees.mixins import AllCommitteesMixin
from legislators.mixins import AllLegislatorsMixin, ChambersMixin
from bills.models import Bill, Subject


class BillDetail(AllSubjectsMixin, AllLegislatorsMixin,
                 ConveneTimeMixin, DetailView):
    model = Bill
    template_name = 'pages/bill.html'


class NewLawsListDetail(AllSubjectsMixin, AllLegislatorsMixin,
                        ConveneTimeMixin, ListView):
    queryset = Bill.objects.filter(became_law__isnull=False)
    template_name = 'pages/new-laws.html'


class VetoedListDetail(AllSubjectsMixin, AllLegislatorsMixin,
                       ConveneTimeMixin, ListView):
    queryset = Bill.objects.filter(vetoed__isnull=False)
    template_name = 'pages/vetoed-bills.html'


class SubjectDetail(AllSubjectsMixin, AllLegislatorsMixin,
                    ConveneTimeMixin, DetailView):
    model = Subject
    template_name = 'pages/subject.html'


class SubjectListDetail(ConveneTimeMixin, ListView):
    model = Subject
    template_name = 'pages/subject-list.html'


class BillSearchView(AllLegislatorsMixin, AllSubjectsMixin,
                     AllCommitteesMixin, ConveneTimeMixin, TemplateView):
    template_name = 'pages/find-bills.html'


class BillSearchJson(ListView):
    queryset = Bill.objects.all().values('name', 'slug')

    def render_to_response(self, context, **kwargs):
        return JsonResponse(list(context['object_list']), safe=False)


class LegeStreamDetail(AllSubjectsMixin, AllLegislatorsMixin,
                       ChambersMixin, ConveneTimeMixin, TemplateView):
    template_name = 'pages/legestream.html'
