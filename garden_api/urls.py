from django.urls import path
from rest_framework.authtoken import views
from .views import RegisterApiView, UserApiView, TestApiView, TestDetailApiView


urlpatterns = [
    path('user/<int:pk>', UserApiView.as_view(), name='user-detail'),
    path('register', RegisterApiView.as_view(), name='register'),
    path('login', views.obtain_auth_token),
    path('test', TestApiView.as_view(), name='test'),
    path('test_detail/<int:pk>', TestDetailApiView.as_view(), name='test_detail')
    # path('current/', CurrentApiView.as_view(), name='current'),
    # path('weekly/', WeeklyApiView.as_view(), name='weekly'),
    # path('monthly/', MonthlyApiView.as_view(), name='monthly'),
]
