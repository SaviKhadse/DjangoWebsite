from django.urls import path
from . import views

from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

urlpatterns = [
	path('', views.home_view, name='home_view'),
	# path('register', views.register_view, name='register_view'),
	# path('form', views.my_form, name='my_form'),
	# path('login', views.login_view, name='login_view'),
]