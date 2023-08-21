from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.greeting, name='home'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('tickets', views.tickets, name='tickets'),
    path('plan/1', views.plan, name='plan1'),
    path('plan/2', views.plan, name='plan2'),
    path('plan/3', views.plan, name='plan3'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
