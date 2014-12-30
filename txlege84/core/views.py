from django.views.generic import ListView

from topics.models import Topic


class LandingView(ListView):
    model = Topic
    template_name = 'landing.html'
