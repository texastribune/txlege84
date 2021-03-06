from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView

from bills.mixins import AllSubjectsMixin
from core.mixins import ConveneTimeMixin
from legislators.mixins import AllLegislatorsMixin

from committees.models import Committee
from legislators.models import Chamber


class CommitteeList(ConveneTimeMixin, ListView):
    model = Committee
    template_name = 'pages/committees-landing.html'


class ChamberCommitteeList(ConveneTimeMixin, DetailView):
    model = Chamber
    template_name = 'pages/chamber-committees.html'


class CommitteeDetail(AllSubjectsMixin, AllLegislatorsMixin,
                      ConveneTimeMixin, DetailView):
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
            queryset = queryset.filter(
                **{slug_field: slug, chamber_field: chamber_slug})

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
