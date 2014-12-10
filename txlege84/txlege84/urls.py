from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from bills.views import BillDetail
from committees.views import CommitteeDetail
from legislators.views import LegislatorDetail

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='landing.html')),
    url(r'^topic-list-landing/$', TemplateView.as_view(template_name='topic-list-landing.html')),
    url(r'^topic-list/$', TemplateView.as_view(template_name='topic-list.html')),
    url(r'^84/bills/(?P<slug>[-\w]+)/$', BillDetail.as_view(), name='bill-detail'),
    url(r'^84/legislators/(?P<slug>[-\w]+)/$', LegislatorDetail.as_view(), name='legislator-detail'),
    url(r'^84/committees/(?P<chamber>[-\w]+)/(?P<slug>[-\w]+)/$', CommitteeDetail.as_view(), name='committee-detail'),
    url(r'^issue/$', TemplateView.as_view(template_name='issue.html')),

    # Examples:
    # url(r'^$', 'txlege84.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the import above and next line to serve media files in development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
