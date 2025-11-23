from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path("", views.recommendation_dashboard, name="recommendation_dashboard"),
    path("career-paths/", views.career_paths, name="career_paths"),
    path("skill-gap-analysis/", views.skill_gap_analysis, name="skill_gap_analysis"),
    path(
        "toggle-favorite/<int:recommendation_id>/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path("save-feedback/", views.save_recommendation_feedback, name="save_feedback"),
]
