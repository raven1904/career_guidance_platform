from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def recommendation_dashboard(request):
    """Simple recommendation dashboard for testing"""

    # Sample data for testing
    sample_recommendations = [
        {
            "id": 1,
            "career_title": "Data Scientist",
            "match_score": 85.5,
            "detailed_scores": {
                "personality": 80,
                "skills": 70,
                "education": 90,
                "market": 85,
            },
            "missing_skills": ["Machine Learning", "Big Data", "Python Advanced"],
            "job_growth": 31,
            "demand_score": 95,
            "remote_friendly": True,
            "category": "Technology",
            "salary_range": {"min": 80000, "max": 180000, "median": 120000},
        },
        {
            "id": 2,
            "career_title": "UX Designer",
            "match_score": 78.2,
            "detailed_scores": {
                "personality": 85,
                "skills": 65,
                "education": 75,
                "market": 80,
            },
            "missing_skills": ["User Research", "Figma", "Prototyping"],
            "job_growth": 18,
            "demand_score": 88,
            "remote_friendly": True,
            "category": "Design",
            "salary_range": {"min": 60000, "max": 130000, "median": 85000},
        },
        {
            "id": 3,
            "career_title": "Software Engineer",
            "match_score": 92.1,
            "detailed_scores": {
                "personality": 88,
                "skills": 95,
                "education": 85,
                "market": 92,
            },
            "missing_skills": ["System Design", "Cloud Computing"],
            "job_growth": 22,
            "demand_score": 98,
            "remote_friendly": True,
            "category": "Technology",
            "salary_range": {"min": 70000, "max": 200000, "median": 110000},
        },
    ]

    # Sample career clusters
    career_clusters = {
        "Technology": [sample_recommendations[0], sample_recommendations[2]],
        "Design": [sample_recommendations[1]],
    }

    context = {
        "recommendations": sample_recommendations,
        "career_clusters": career_clusters,
    }

    return render(request, "recommendations/dashboard.html", context)


@login_required
def career_paths(request):
    """Career paths page"""
    return render(request, "recommendations/career_paths.html")


@login_required
def skill_gap_analysis(request):
    """Skill gap analysis page"""
    target_career = request.GET.get("career", "Data Scientist")

    # Sample data
    context = {
        "target_career": target_career,
        "progress_percentage": 45,
        "missing_skills": ["Machine Learning", "Python Advanced", "Statistics"],
        "learning_path": {
            "priority_skills": ["Python", "Machine Learning", "Statistics"],
            "recommended_courses": [
                "Python for Data Science",
                "Machine Learning Fundamentals",
                "Statistics for Data Analysis",
            ],
            "timeline_estimate": "3-6 months",
            "resources": ["Data Science Handbook", "Online tutorials"],
        },
        "career_details": {
            "salary_range": {"min": 80000, "max": 180000, "median": 120000},
            "job_growth": 31,
            "demand_score": 95,
        },
    }

    return render(request, "recommendations/skill_gap.html", context)


@login_required
def toggle_favorite(request, recommendation_id):
    """Toggle favorite status - simple version"""
    return JsonResponse({"success": True, "is_favorite": True})


@login_required
def save_recommendation_feedback(request):
    """Save feedback - simple version"""
    return JsonResponse({"success": True, "message": "Feedback saved!"})
