from legislators.models import Legislator


class AllLegislatorsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllLegislatorsMixin, self).get_context_data(**kwargs)
        context['rep_list'] = Legislator.objects.filter(
            chamber__name='Texas House').order_by('last_name')
        context['sen_list'] = Legislator.objects.filter(
            chamber__name='Texas Senate').order_by('last_name')
        return context
