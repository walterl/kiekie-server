from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from kiekie.api import views


router = DefaultRouter()
router.register('pics', views.PictureViewSet)

urlpatterns = [
    url('^user/login$', views.login),
    url('^user/logout$', views.logout),
    url('^user/register$', views.api_register),
    url('', include(router.urls)),
]
