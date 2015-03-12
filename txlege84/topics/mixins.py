from topics.models import FeaturedTopic


class FeaturedTopicMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FeaturedTopicMixin, self).get_context_data(**kwargs)
        context['featured_topic'] = FeaturedTopic.objects.first()
        return context
