from django.views.generic import ListView

from core.mixins import ConveneTimeMixin
from topics.mixins import FeaturedTopicMixin

from topics.models import FeaturedTopic, Topic


class LandingView(FeaturedTopicMixin, ConveneTimeMixin, ListView):
    template_name = 'landing.html'

    def get_queryset(self):
        # only returns the one not considered a featured topic
        return Topic.objects.exclude(id=FeaturedTopic.objects.first().topic.id)
