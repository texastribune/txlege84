from django.views.generic import DetailView, ListView

from topics.models import Issue, Topic


class TopicListDetail(ListView):
    model = Topic
    template_name = 'pages/topic-list-landing.html'


class TopicDetail(DetailView):
    model = Topic
    template_name = 'pages/topic-list.html'

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()
        return context


class IssueDetail(DetailView):
    model = Issue
    template_name = 'pages/issue.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()
        return context
