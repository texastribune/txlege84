from django.views.generic import DetailView, ListView

from topics.models import Issue, Topic


class AllTopicsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllTopicsMixin, self).get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()
        return context


class TopicListDetail(ListView):
    model = Topic
    template_name = 'pages/topic-list-landing.html'


class TopicDetail(AllTopicsMixin, DetailView):
    model = Topic
    template_name = 'pages/topic-list.html'


class IssueDetail(AllTopicsMixin, DetailView):
    model = Issue
    template_name = 'pages/issue.html'
