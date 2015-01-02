from django.views.generic import ListView

from topics.models import Topic, TopIssue


class LandingView(ListView):
    model = Topic
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['top_issues'] = TopIssue.objects.all()[:4]
        return context
