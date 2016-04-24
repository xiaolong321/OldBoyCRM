from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    url(r'^Customer/$',
        login_required(views.Customer_View.as_view()),
        name='Customer_List'
        ),

]