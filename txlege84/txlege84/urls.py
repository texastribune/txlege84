from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='landing.html')),
    url(r'^topic-list-landing/$', TemplateView.as_view(template_name='topic-list-landing.html')),
    url(r'^topic-list/$', TemplateView.as_view(template_name='topic-list.html')),
    url(r'^bill/$', TemplateView.as_view(template_name='bill.html')),
    url(r'^legislator/$', TemplateView.as_view(template_name='legislator.html')),
    url(r'^committee/$', TemplateView.as_view(template_name='committee.html')),

    # Examples:
    # url(r'^$', 'txlege84.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the import above and next line to serve media files in development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
