from django.urls import path

# importing views from views..py
from .views import home_view, result_view

urlpatterns = [
	path('', home_view ),
	path('result.html', result_view)
]

