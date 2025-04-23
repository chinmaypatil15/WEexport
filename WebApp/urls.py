from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('metal/', views.metal, name='metal'),
    path('agro-commodities/', views.agro_commodities, name='agro_commodities'),
    path('industrialproduct/', views.industrialproduct, name='industrialproduct'),
    path('frozen-foods/', views.frozen_foods, name='frozen_foods'),
]
