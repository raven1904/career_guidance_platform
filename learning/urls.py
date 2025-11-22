from django.urls import path
from . import views

urlpatterns = [
    path("", views.learning_dashboard, name="learning_dashboard"),
    path("courses/", views.course_recommendations, name="course_recommendations"),
    path("learning-paths/", views.learning_paths, name="learning_paths"),
]
