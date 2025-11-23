import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class CareerAIEngine:
    def __init__(self):
        # Sample career database - in production, this would be from a proper database
        self.career_data = self.load_career_data()
        self.vectorizer = TfidfVectorizer()
        
    def load_career_data(self):
        return [
            {
                'title': 'Data Scientist',
                'skills': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis'],
                'personality_traits': ['INTJ', 'INTP', 'ENTJ'],
                'demand_score': 95,
                'salary_range': {'min': 80000, 'max': 150000},
                'growth_projection': 25,
                'description': 'Analyze and interpret complex data to help organizations make decisions'
            },
            {
                'title': 'Software Engineer',
                'skills': ['Programming', 'Algorithms', 'System Design', 'Testing', 'Debugging'],
                'personality_traits': ['INTJ', 'ISTJ', 'ENTJ', 'ESTJ'],
                'demand_score': 98,
                'salary_range': {'min': 70000, 'max': 160000},
                'growth_projection': 22,
                'description': 'Design, develop, and maintain software systems'
            },
            {
                'title': 'UX Designer',
                'skills': ['User Research', 'Wireframing', 'Prototyping', 'UI Design', 'User Testing'],
                'personality_traits': ['ENFP', 'INFJ', 'INFP', 'ENFJ'],
                'demand_score': 90,
                'salary_range': {'min': 65000, 'max': 120000},
                'growth_projection': 18,
                'description': 'Create user-centered designs for digital products'
            }
        ]
    
    def calculate_personality_compatibility(self, user_personality, career_traits):
        """Calculate compatibility between user personality and career traits"""
        if not user_personality or not career_traits:
            return 0.5
            
        # Simple matching - enhance with proper personality theory
        matches = sum(1 for trait in career_traits if user_personality in trait)
        return matches / len(career_traits) if career_traits else 0
    
    def calculate_skill_match(self, user_skills, required_skills):
        """Calculate skill match percentage"""
        if not user_skills or not required_skills:
            return 0
            
        user_skill_list = [skill.strip().lower() for skill in user_skills.split(',')]
        required_skill_list = [skill.lower() for skill in required_skills]
        
        matches = sum(1 for skill in required_skill_list if any(user_skill in skill for user_skill in user_skill_list))
        return matches / len(required_skill_list)
    
    def generate_recommendations(self, user_data):
        """Generate career recommendations based on user data"""
        recommendations = []
        
        for career in self.career_data:
            # Calculate compatibility scores
            personality_score = self.calculate_personality_compatibility(
                user_data.get('personality_type'), 
                career['personality_traits']
            )
            
            skill_score = self.calculate_skill_match(
                user_data.get('skills', ''),
                career['skills']
            )
            
            # Combined score (weighted average)
            total_score = (personality_score * 0.4 + skill_score * 0.4 + 
                          career['demand_score'] / 100 * 0.2)
            
            # Skill gap analysis
            user_skills = [skill.strip().lower() for skill in user_data.get('skills', '').split(',')] if user_data.get('skills') else []
            missing_skills = [skill for skill in career['skills'] if not any(user_skill in skill.lower() for user_skill in user_skills)]
            
            recommendations.append({
                'career': career['title'],
                'match_score': round(total_score * 100, 2),
                'personality_compatibility': round(personality_score * 100, 2),
                'skill_match': round(skill_score * 100, 2),
                'description': career['description'],
                'salary_range': career['salary_range'],
                'growth_projection': career['growth_projection'],
                'missing_skills': missing_skills,
                'demand_score': career['demand_score']
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:10]  # Return top 10 recommendations

# Global instance
ai_engine = CareerAIEngine()