from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recommendations.models import CareerRecommendation
from assessments.models import Assessment, AssessmentResult

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate test data for development'

    def handle(self, *args, **options):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'password': 'testpass123'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create sample recommendations
        sample_data = [
            {
                'career_title': 'Data Scientist',
                'match_score': 85.5,
                'detailed_scores': {'personality': 80, 'skills': 70, 'education': 90, 'market': 85},
                'missing_skills': ['Machine Learning', 'Big Data', 'Python Advanced'],
                'demand_score': 95,
                'job_growth': 31,
                'remote_friendly': True
            },
            {
                'career_title': 'UX Designer',
                'match_score': 78.2,
                'detailed_scores': {'personality': 85, 'skills': 65, 'education': 75, 'market': 80},
                'missing_skills': ['User Research', 'Figma', 'Prototyping'],
                'demand_score': 88,
                'job_growth': 18,
                'remote_friendly': True
            },
            {
                'career_title': 'Software Engineer',
                'match_score': 92.1,
                'detailed_scores': {'personality': 88, 'skills': 95, 'education': 85, 'market': 92},
                'missing_skills': ['System Design', 'Cloud Computing'],
                'demand_score': 98,
                'job_growth': 22,
                'remote_friendly': True
            }
        ]

        for data in sample_data:
            rec, created = CareerRecommendation.objects.get_or_create(
                user=user,
                career_title=data['career_title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created recommendation: {data["career_title"]}'))

        self.stdout.write(self.style.SUCCESS('Test data generation completed!'))