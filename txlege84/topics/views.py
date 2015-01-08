from django.views.generic import DetailView, ListView

from bills.mixins import AllSubjectsMixin
from topics.models import Issue, Topic


class AllTopicsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllTopicsMixin, self).get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()
        return context


class TopicListDetail(AllSubjectsMixin, ListView):
    model = Topic
    template_name = 'pages/topic-list-landing.html'


class TopicDetail(AllSubjectsMixin, AllTopicsMixin, DetailView):
    model = Topic
    template_name = 'pages/topic-list.html'


class IssueDetail(AllSubjectsMixin, AllTopicsMixin, DetailView):
    model = Issue
    template_name = 'pages/issue.html'
