from legislators.models import Legislator


class AllLegislatorsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllLegislatorsMixin, self).get_context_data(**kwargs)
        context['legislator_list'] = Legislator.objects.all()
        return context
