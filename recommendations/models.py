from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CareerRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='career_recommendations')
    career_title = models.CharField(max_length=200)
    match_score = models.FloatField()
    detailed_scores = models.JSONField(default=dict)
    missing_skills = models.JSONField(default=list)
    learning_path = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    feedback_score = models.IntegerField(null=True, blank=True)  # 1-5 rating
    
    class Meta:
        ordering = ['-match_score']
    
    def __str__(self):
        return f"{self.user.username} - {self.career_title} ({self.match_score}%)"

class SkillGapAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_gaps')
    target_career = models.CharField(max_length=200)
    current_skills = models.JSONField(default=list)
    required_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    priority_skills = models.JSONField(default=list)
    progress_percentage = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.target_career} Skill Gap"

class LearningPath(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    career_target = models.CharField(max_length=200)
    courses = models.JSONField(default=list)
    resources = models.JSONField(default=list)
    timeline = models.CharField(max_length=100)
    progress = models.FloatField(default=0.0)
    estimated_completion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.career_target} Learning Path"

class IndustryTrend(models.Model):
    industry = models.CharField(max_length=100)
    growth_rate = models.FloatField()
    average_salary = models.JSONField(default=dict)
    in_demand_skills = models.JSONField(default=list)
    remote_work_percentage = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.industry} Trends"