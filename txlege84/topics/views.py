from django.views.generic import DetailView, ListView

from bills.mixins import AllSubjectsMixin
from core.mixins import ConveneTimeMixin
from legislators.mixins import AllLegislatorsMixin
from topics.models import Issue, Topic


class AllTopicsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllTopicsMixin, self).get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()
        return context


class TopicListDetail(AllSubjectsMixin, AllLegislatorsMixin,
                      ConveneTimeMixin, ListView):
    model = Topic
    template_name = 'pages/topic-list-landing.html'


class TopicDetail(AllSubjectsMixin, AllTopicsMixin, AllLegislatorsMixin,
                  ConveneTimeMixin, DetailView):
    model = Topic
    template_name = 'pages/topic-list.html'


class IssueDetail(AllSubjectsMixin, AllTopicsMixin, AllLegislatorsMixin,
                  ConveneTimeMixin, DetailView):
    model = Issue
    template_name = 'pages/issue.html'
