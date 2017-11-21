from django.conf.urls import include,url
from django.contrib import admin
from dashing.utils import router


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^weather/', include('weather.urls')),
    url(r'^dashboard/', include(router.urls)),
]
