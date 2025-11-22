from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def job_listings(request):
    return render(request, "jobs/listings.html")


@login_required
def application_tracking(request):
    return render(request, "jobs/applications.html")


@login_required
def salary_insights(request):
    return render(request, "jobs/salary.html")
