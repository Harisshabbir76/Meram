from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/corporate-events/', views.corporate_events, name='corporate_events'),
    path('services/other-services/', views.other_services, name='other_services'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('book-now/', views.book_now, name='book_now'),
]
