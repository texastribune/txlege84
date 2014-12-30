from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from bills.views import BillDetail
from core.views import LandingView
from committees.views import CommitteeDetail
from legislators.views import LegislatorDetail
from topics.views import IssueDetail, TopicDetail, TopicListDetail

urlpatterns = patterns(
    '',
    url(r'^$', LandingView.as_view(), name='landing-view'),
    url(r'^84/hot-lists/$',
        TopicListDetail.as_view(), name='topic-list-detail'),
    url(r'^84/hot-lists/(?P<slug>[-\w]+)/$',
        TopicDetail.as_view(), name='topic-detail'),
    url(r'^84/hot-lists/(?P<hot_list_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        IssueDetail.as_view(), name='issue-detail'),
    url(r'^84/bills/(?P<slug>[-\w]+)/$',
        BillDetail.as_view(), name='bill-detail'),
    url(r'^84/legislators/(?P<slug>[-\w]+)/$',
        LegislatorDetail.as_view(), name='legislator-detail'),
    url(r'^84/committees/(?P<chamber>[-\w]+)/(?P<slug>[-\w]+)/$',
        CommitteeDetail.as_view(), name='committee-detail'),

    # Examples:
    # url(r'^$', 'txlege84.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # FOR DEVELOPMENT:
    url(r'^hot-list/$', TemplateView.as_view(
        template_name='pages/topic-list-landing.html')),
    url(r'^hot-list-detail/$', TemplateView.as_view(
        template_name='pages/topic-list.html')),
    url(r'^issue-detail/$', TemplateView.as_view(
        template_name='pages/issue.html')),
)

# Uncomment the import above and next line to serve media files in development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
