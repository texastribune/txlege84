from django.views.generic import ListView

from topics.models import Topic


class LandingView(ListView):
    model = Topic
    template_name = 'landing.html'

    # def get_context_data(self, **kwargs):
    #     context = super(TopicList, self).get_context_data(**kwargs)
    #     context['issueList'] = Topic.objects.issue.all()
    #     return context
