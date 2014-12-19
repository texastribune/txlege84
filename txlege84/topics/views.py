from django.views.generic import DetailView, ListView

from topics.models import Issue, Topic


class TopicListDetail(ListView):
    model = Topic
    template_name = 'pages/topic-list-landing.html'


class TopicDetail(DetailView):
    model = Topic
    template_name = 'pages/topic-list.html'


class IssueDetail(DetailView):
    model = Issue
    template_name = 'pages/issue.html'
