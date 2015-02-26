from committees.models import Committee


class AllCommitteesMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllCommitteesMixin, self).get_context_data(**kwargs)
        context['committee_list'] = Committee.objects.all()
        return context
