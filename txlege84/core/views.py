from django.views.generic import ListView

from topics.models import Topic


class TopicList(ListView):
    model = Topic
    template_name = 'landing.html'


# class TopicListDetail(ListView):
#     model = Topic
#     template_name = 'landing.html'

#     def get_context_data(self, **kwargs):
#         context = super(TopicListDetail, self).get_context_data(**kwargs)
#         context['hotList'] = Topic.objects.all()
#         return context
