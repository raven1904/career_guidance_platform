from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_listings, name="job_listings"),
    path("applications/", views.application_tracking, name="application_tracking"),
    path("salary-insights/", views.salary_insights, name="salary_insights"),
]
