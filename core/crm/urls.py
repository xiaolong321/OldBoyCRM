from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from .web_views import views
urlpatterns = [
    url(r'^$',
        login_required(views.CrmIndexView.as_view()),
        name='crm_index'
        ),
    url(r'^api/', include("core.crm.web_api.urls",
                           namespace="api")),
    url(r'^pages/', include("core.crm.web_views.urls",
                            namespace="pages")),
]