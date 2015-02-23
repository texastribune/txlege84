from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView

from django.contrib import admin

from bills.views import (BillDetail, BillSearchJson,
                         SubjectDetail, LegeStreamDetail)
from core.views import LandingView
from committees.views import CommitteeDetail
from explainers.views import ExplainerListDetail
from legislators.views import LegislatorDetail
from topics.views import IssueDetail, TopicDetail, TopicListDetail

urlpatterns = patterns(
    '',
    url(r'^$', LandingView.as_view(), name='landing-view'),
    url(r'^topics/$',
        TopicListDetail.as_view(), name='topic-list-detail'),
    url(r'^topics/(?P<slug>[-\w]+)/$',
        TopicDetail.as_view(), name='topic-detail'),
    url(r'^topics/(?P<hot_list_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        IssueDetail.as_view(), name='issue-detail'),
    url(r'^84/bills/(?P<slug>[-\w]+)/$',
        BillDetail.as_view(), name='bill-detail'),
    url(r'^84/categories/(?P<slug>[-\w]+)/$',
        SubjectDetail.as_view(), name='category-detail'),
    url(r'^84/legislators/(?P<slug>[-\w]+)/$',
        LegislatorDetail.as_view(), name='legislator-detail'),
    url(r'^84/committees/(?P<chamber>[-\w]+)/(?P<slug>[-\w]+)/$',
        CommitteeDetail.as_view(), name='committee-detail'),
    url(r'^how-session-works/$',
        ExplainerListDetail.as_view(), name='explainer-list-detail'),
    url(r'^livestream/$',
        LegeStreamDetail.as_view(), name='legestream'),
    url(r'^search/bills/', BillSearchJson.as_view(), name='bill-search'),

    # Redirects
    # Note: /hot-lists/ landing won't exist in 2.0
    # Create another redirect for /topics/ to landing index before launch
    # And change /hot-lists/ to landing index
    url(r'^hot-lists/$',
        RedirectView.as_view(url='../topics')),
    url(r'^hot-lists/(?P<slug>[-\w]+)/$',
        RedirectView.as_view(url='../../topics/%(slug)s/')),
    url(r'^hot-lists/(?P<hot_list_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        RedirectView.as_view(url='../../../topics/%(hot_list_slug)s/%(slug)s/')),
    url(r'^legestream/$',
        RedirectView.as_view(url='../livestream/')),
    url(r'^texplainers/$',
        RedirectView.as_view(url='../how-session-works/')),

    # Examples:
    # url(r'^$', 'txlege84.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
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
