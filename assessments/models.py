from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Assessment(models.Model):
    ASSESSMENT_TYPES = (
        ("personality", "Personality Assessment"),
        ("skills", "Skills Assessment"),
        ("interests", "Interests Assessment"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    questions_count = models.IntegerField(default=0)
    time_required = models.IntegerField(help_text="Time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    order = models.IntegerField(default=0)
    question_type = models.CharField(max_length=50, default="multiple_choice")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}..."


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    text = models.CharField(max_length=200)
    value = models.CharField(max_length=50, help_text="Value for scoring")
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.text


class AssessmentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.JSONField(help_text="Stores scores in JSON format")
    completed_at = models.DateTimeField(auto_now_add=True)
    personality_type = models.CharField(max_length=10, blank=True)
    dominant_traits = models.JSONField(default=list)

    class Meta:
        unique_together = ["user", "assessment"]

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title}"
