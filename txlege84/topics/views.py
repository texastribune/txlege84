from django.views.generic import DetailView, ListView

from bills.mixins import AllSubjectsMixin
from legislators.mixins import AllLegislatorsMixin
from topics.models import Issue, Topic


class AllTopicsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllTopicsMixin, self).get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()
        return context


class TopicListDetail(AllSubjectsMixin, AllLegislatorsMixin, ListView):
    model = Topic
    template_name = 'pages/topic-list-landing.html'


class TopicDetail(AllSubjectsMixin, AllTopicsMixin, AllLegislatorsMixin, DetailView):
    model = Topic
    template_name = 'pages/topic-list.html'


class IssueDetail(AllSubjectsMixin, AllTopicsMixin, AllLegislatorsMixin, DetailView):
    model = Issue
    template_name = 'pages/issue.html'
