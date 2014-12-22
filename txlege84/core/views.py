from django.views.generic import TemplateView, ListView

from topics.models import Issue, Topic


class LandingDetail(TemplateView):
    model = Issue
    template_name = 'landing.html'


class TopicListDetail(ListView):
    model = Topic
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super(TopicListDetail, self).get_context_data(**kwargs)
        context['hot-list'] = Topic.objects.all()
        return context
