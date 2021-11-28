from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'order', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
