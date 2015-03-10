from core.models import ConveneTime


class ConveneTimeMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ConveneTimeMixin, self).get_context_data(**kwargs)
        context['house_convene'] = ConveneTime.objects.get(
            chamber__name='Texas House')
        context['senate_convene'] = ConveneTime.objects.get(
            chamber__name='Texas Senate')
        return context
