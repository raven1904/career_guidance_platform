import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Assessment, AssessmentResult, Question, Choice
from .ai_engine import ai_engine

@login_required
def assessment_list(request):
    assessments = Assessment.objects.filter(is_active=True)
    completed_assessments = AssessmentResult.objects.filter(
        user=request.user
    ).values_list('assessment_id', flat=True)
    
    return render(request, 'assessments/assessment_list.html', {
        'assessments': assessments,
        'completed_assessments': completed_assessments
    })

@login_required
def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, is_active=True)
    questions = assessment.questions.all().prefetch_related('choices')
    
    # Check if already completed
    existing_result = AssessmentResult.objects.filter(
        user=request.user, 
        assessment=assessment
    ).first()
    
    if request.method == 'POST':
        answers = {}
        total_score = 0
        
        for question in questions:
            answer_key = f'question_{question.id}'
            answer = request.POST.get(answer_key)
            if answer:
                try:
                    choice = Choice.objects.get(id=answer)
                    answers[str(question.id)] = {
                        'choice_id': choice.id,
                        'value': choice.value,
                        'weight': float(choice.weight),
                        'question_text': question.text,
                        'choice_text': choice.text
                    }
                    total_score += choice.weight
                except Choice.DoesNotExist:
                    pass
        
        # Calculate personality type
        personality_type = calculate_personality_type(answers)
        
        # Generate career recommendations
        user_data = {
            'personality_type': personality_type,
            'skills': request.user.studentprofile.skills if hasattr(request.user, 'studentprofile') else ''
        }
        
        career_recommendations = ai_engine.generate_recommendations(user_data)
        
        # Save results
        result, created = AssessmentResult.objects.update_or_create(
            user=request.user,
            assessment=assessment,
            defaults={
                'score': answers,
                'personality_type': personality_type,
                'dominant_traits': get_dominant_traits(answers),
                'career_recommendations': career_recommendations
            }
        )
        
        # Update student profile if exists
        if hasattr(request.user, 'studentprofile'):
            student_profile = request.user.studentprofile
            student_profile.personality_type = personality_type
            student_profile.dominant_skills = get_dominant_traits(answers)
            student_profile.save()
        
        messages.success(request, 'Assessment completed successfully!')
        return render(request, 'assessments/assessment_result.html', {
            'result': result,
            'assessment': assessment,
            'recommendations': career_recommendations
        })
    
    return render(request, 'assessments/take_assessment.html', {
        'assessment': assessment,
        'questions': questions,
        'existing_result': existing_result
    })

@login_required
def assessment_results(request, result_id):
    result = get_object_or_404(AssessmentResult, id=result_id, user=request.user)
    return render(request, 'assessments/assessment_result.html', {
        'result': result,
        'recommendations': result.career_recommendations
    })

# Helper functions
def calculate_personality_type(answers):
    """Enhanced MBTI calculation"""
    dimensions = {
        'EI': {'E': 0, 'I': 0},  # Extraversion vs Introversion
        'SN': {'S': 0, 'N': 0},  # Sensing vs Intuition
        'TF': {'T': 0, 'F': 0},  # Thinking vs Feeling
        'JP': {'J': 0, 'P': 0},  # Judging vs Perceiving
    }
    
    for answer_data in answers.values():
        value = answer_data['value']
        weight = answer_data['weight']
        
        if value in ['E', 'I']:
            dimensions['EI'][value] += weight
        elif value in ['S', 'N']:
            dimensions['SN'][value] += weight
        elif value in ['T', 'F']:
            dimensions['TF'][value] += weight
        elif value in ['J', 'P']:
            dimensions['JP'][value] += weight
    
    personality = ''
    personality += 'E' if dimensions['EI']['E'] > dimensions['EI']['I'] else 'I'
    personality += 'S' if dimensions['SN']['S'] > dimensions['SN']['N'] else 'N'
    personality += 'T' if dimensions['TF']['T'] > dimensions['TF']['F'] else 'F'
    personality += 'J' if dimensions['JP']['J'] > dimensions['JP']['P'] else 'P'
    
    return personality

def get_dominant_traits(answers):
    trait_count = {}
    for answer_data in answers.values():
        value = answer_data['value']
        trait_count[value] = trait_count.get(value, 0) + 1
    
    return [{'trait': trait, 'count': count} for trait, count in sorted(
        trait_count.items(), key=lambda x: x[1], reverse=True
    )[:5]]