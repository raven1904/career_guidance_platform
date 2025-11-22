import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Assessment, AssessmentResult, Question, Choice


@login_required
def assessment_list(request):
    assessments = Assessment.objects.filter(is_active=True)
    return render(
        request, "assessments/assessment_list.html", {"assessments": assessments}
    )


@login_required
def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, is_active=True)
    questions = assessment.questions.all().prefetch_related("choices")

    if request.method == "POST":
        # Process assessment results
        answers = {}
        total_score = 0

        for question in questions:
            answer_key = f"question_{question.id}"
            answer = request.POST.get(answer_key)
            if answer:
                try:
                    choice = Choice.objects.get(id=answer)
                    answers[question.id] = {
                        "choice_id": choice.id,
                        "value": choice.value,
                        "weight": choice.weight,
                    }
                    total_score += choice.weight
                except Choice.DoesNotExist:
                    pass

        # Calculate personality type (simplified MBTI)
        personality_type = calculate_personality_type(answers)

        # Save results
        result, created = AssessmentResult.objects.update_or_create(
            user=request.user,
            assessment=assessment,
            defaults={
                "score": answers,
                "personality_type": personality_type,
                "dominant_traits": get_dominant_traits(answers),
            },
        )

        return render(
            request,
            "assessments/assessment_result.html",
            {"result": result, "assessment": assessment},
        )

    return render(
        request,
        "assessments/take_assessment.html",
        {"assessment": assessment, "questions": questions},
    )


def calculate_personality_type(answers):
    """
    Simplified MBTI personality type calculation
    This is a basic implementation - you can enhance this with proper algorithms
    """
    # This is a simplified version - implement proper MBTI scoring
    traits = {
        "E": 0,
        "I": 0,  # Extraversion vs Introversion
        "S": 0,
        "N": 0,  # Sensing vs Intuition
        "T": 0,
        "F": 0,  # Thinking vs Feeling
        "J": 0,
        "P": 0,  # Judging vs Perceiving
    }

    # Map choice values to traits and accumulate scores
    for answer_data in answers.values():
        value = answer_data["value"]
        weight = answer_data["weight"]

        if value in traits:
            traits[value] += weight

    # Determine personality type
    personality = ""
    personality += "E" if traits["E"] > traits["I"] else "I"
    personality += "S" if traits["S"] > traits["N"] else "N"
    personality += "T" if traits["T"] > traits["F"] else "F"
    personality += "J" if traits["J"] > traits["P"] else "P"

    return personality


def get_dominant_traits(answers):
    """Extract dominant traits from answers"""
    trait_count = {}
    for answer_data in answers.values():
        value = answer_data["value"]
        trait_count[value] = trait_count.get(value, 0) + 1

    # Return top 5 traits
    return sorted(trait_count.items(), key=lambda x: x[1], reverse=True)[:5]
