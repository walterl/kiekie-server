from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from kiekie.api import views


router = DefaultRouter()
router.register('pics', views.PictureViewSet)

urlpatterns = [url('', include(router.urls))]
