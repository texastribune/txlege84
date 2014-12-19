from django.views.generic import DetailView

from topics.models import Topic


class TopicDetail(DetailView):
    model = Topic
    template_name = 'topic-list.html'
