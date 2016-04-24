from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/', include("core.crm.web_api.urls",
                           namespace="api")),
    url(r'^pages/', include("core.crm.web_views.urls",
                            namespace="pages")),
]