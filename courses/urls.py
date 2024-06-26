from django.urls import path
from . import views

urlpatterns = [
    path('join_course/<uuid:course_id>/', views.JoinCourse.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('login/email-password/', views.EmailPasswordLogin.as_view())
]