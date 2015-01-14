from legislators.models import Chamber, Legislator


class AllLegislatorsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllLegislatorsMixin, self).get_context_data(**kwargs)
        context['rep_list'] = Legislator.objects.filter(
            chamber__name='Texas House').order_by('last_name').active()
        context['sen_list'] = Legislator.objects.filter(
            chamber__name='Texas Senate').order_by('last_name').active()
        return context


class ChambersMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ChambersMixin, self).get_context_data(**kwargs)
        context['house'] = Chamber.objects.get(name='Texas House')
        context['senate'] = Chamber.objects.get(name='Texas Senate')
        return context
