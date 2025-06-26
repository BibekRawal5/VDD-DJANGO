from django.urls import path

# importing views from views..py
from .views import home_view, contact_view, about_view, result_view

urlpatterns = [
	path('', home_view, name='home'),
	path('contact.html', contact_view, name='contact'),
	path('about.html', about_view, name='about'),
	path('result.html', result_view, name='result')
]

