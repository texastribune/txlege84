from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView

from bills.mixins import AllSubjectsMixin
from legislators.mixins import AllLegislatorsMixin
from committees.models import Committee


class CommitteeDetail(AllSubjectsMixin, AllLegislatorsMixin, DetailView):
    model = Committee
    template_name = 'pages/committee.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        chamber_slug = self.kwargs.get('chamber', None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if slug is not None and chamber_slug is not None:
            chamber_field = 'chamber__slug'
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug, chamber_field: chamber_slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "both a chamber_slug and a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
