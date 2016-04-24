from django.conf.urls import include, url
from . import issus
urlpatterns = [
    url(r'issus/', issus.chuliqi, name='issus' )

]