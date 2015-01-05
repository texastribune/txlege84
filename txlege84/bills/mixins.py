from bills.models import Subject


class AllSubjectsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllSubjectsMixin, self).get_context_data(**kwargs)
        context['subject_list'] = Subject.objects.all()
        return context
