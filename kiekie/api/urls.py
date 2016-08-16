from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from kiekie.api import views


router = DefaultRouter()
router.register('pics', views.PictureViewSet)

urlpatterns = [
    url('^user/login$', obtain_auth_token),
    url('^user/register$', views.api_register),
    url('', include(router.urls)),
]
