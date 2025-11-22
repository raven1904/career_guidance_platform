from django.urls import path
from . import views

urlpatterns = [
    path("", views.recommendation_dashboard, name="recommendation_dashboard"),
    path("career-paths/", views.career_paths, name="career_paths"),
    path("skill-gap-analysis/", views.skill_gap_analysis, name="skill_gap_analysis"),
]
