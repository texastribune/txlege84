from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

from bills.views import (BillDetail, BillSearchView, BillSearchJson,
                         SubjectDetail, SubjectListDetail, LegeStreamDetail,
                         VetoedListDetail)
from core.views import LandingView
from committees.views import (ChamberCommitteeList,
                              CommitteeDetail, CommitteeList)
from explainers.views import ExplainerDetail, ExplainerListDetail
from legislators.views import LegislatorDetail, LegislatorList
from topics.views import IssueDetail, TopicDetail

urlpatterns = patterns(
    '',

    # Landing page
    url(r'^$', LandingView.as_view(), name='landing-view'),

    # Topic pages
    url(r'^topics/(?P<hot_list_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        IssueDetail.as_view(), name='issue-detail'),
    url(r'^topics/(?P<slug>[-\w]+)/$',
        TopicDetail.as_view(), name='topic-detail'),
    url(r'^topics/$',
        RedirectView.as_view(pattern_name='landing-view')),

    # Bill pages
    url(r'^84/bills/vetoed-bills/$', VetoedListDetail.as_view(), name='find-bills'),
    url(r'^84/bills/(?P<slug>[-\w]+)/$',
        BillDetail.as_view(), name='bill-detail'),
    url(r'^84/bills/$', BillSearchView.as_view(), name='find-bills'),


    # Subject pages
    url(r'^84/categories/(?P<slug>[-\w]+)/$',
        SubjectDetail.as_view(), name='category-detail'),
    url(r'^84/categories/$',
        SubjectListDetail.as_view(), name='category-list-detail'),

    # Legislator pages
    url(r'^84/legislators/(?P<slug>[-\w]+)/$',
        LegislatorDetail.as_view(), name='legislator-detail'),
    url(r'^84/legislators/$',
        LegislatorList.as_view(), name='legislator-landing'),

    # Committee pages
    url(r'^84/committees/(?P<chamber>[-\w]+)/(?P<slug>[-\w]+)/$',
        CommitteeDetail.as_view(), name='committee-detail'),
    url(r'^84/committees/(?P<slug>[-\w]+)/$',
        ChamberCommitteeList.as_view(), name='chamber-committees'),
    url(r'^84/committees/$',
        CommitteeList.as_view(), name='committees-landing'),

    # Explainer pages
    url(r'^how-session-works/$',
        ExplainerListDetail.as_view(), name='explainer-list-detail'),
    url(r'^how-session-works/(?P<slug>[-\w]+)/$',
        ExplainerDetail.as_view(), name='explainer-detail'),

    # Livestream pages
    url(r'^livestream/$',
        LegeStreamDetail.as_view(), name='legestream'),

    # JSON feed for bill search
    url(r'^search/bills/', BillSearchJson.as_view(), name='bill-search'),

    # Redirects
    url(r'^hot-lists/$',
        RedirectView.as_view(pattern_name='landing-view')),
    url(r'^hot-lists/(?P<slug>[-\w]+)/$',
        RedirectView.as_view(pattern_name='topic-detail')),
    url(r'^hot-lists/(?P<hot_list_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        RedirectView.as_view(pattern_name='issue-detail')),
    url(r'^legestream/$', RedirectView.as_view(pattern_name='legestream')),
    url(r'^texplainers/$',
        RedirectView.as_view(pattern_name='explainer-list-detail')),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the import above and next line to serve media files in development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
