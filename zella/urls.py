from django.urls import path
from . import views

app_name = 'zella'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('quizes/', views.quizes, name='quizes'),
    path('startquiz/<int:quiz_id>/', views.startquiz, name='startquiz'),
    path('profile/', views.profile, name='profile'),
    path('units/', views.units, name='units'),
    path('courses/', views.courses, name='courses'),
    path('register_unit/<int:student_id>/<int:unit_id>/', views.register_unit, name='register_unit'),
    path('submit_assignment/<int:student_id>/<int:quiz_id>/', views.submit_assignment, name='submit_assignment'),
    path('grades/<int:student_id>', views.grades, name='grades')
]