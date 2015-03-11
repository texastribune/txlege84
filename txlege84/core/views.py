from django.views.generic import ListView

from core.mixins import ConveneTimeMixin
from topics.mixins import FeaturedTopicMixin

from topics.models import Topic


class LandingView(FeaturedTopicMixin, ConveneTimeMixin, ListView):
    # only returns the one not considered a featured topic
    queryset = Topic.objects.filter(featured_topic__isnull=True)
    template_name = 'landing.html'
