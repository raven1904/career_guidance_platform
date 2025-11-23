import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AdvancedCareerAI:
    def __init__(self):
        self.career_database = self.load_career_database()
        self.skill_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.personality_mapping = self.load_personality_mapping()
        self.industry_trends = self.load_industry_trends()
        
    def load_career_database(self):
        """Load comprehensive career database"""
        return [
            {
                'id': 1,
                'title': 'Data Scientist',
                'category': 'Technology',
                'skills': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis', 
                          'Deep Learning', 'Data Visualization', 'Big Data', 'R', 'TensorFlow'],
                'personality_traits': ['INTJ', 'INTP', 'ENTJ', 'ISTJ'],
                'education_required': "Bachelor's in Computer Science or related field",
                'experience_level': 'Mid to Senior',
                'salary_range': {'min': 80000, 'max': 180000, 'median': 120000},
                'job_growth': 31,
                'demand_score': 95,
                'remote_friendly': True,
                'stress_level': 'Medium-High',
                'description': 'Analyze and interpret complex digital data to assist in decision-making',
                'day_to_day': ['Building ML models', 'Data cleaning', 'Statistical analysis', 'Team collaboration'],
                'companies': ['Google', 'Amazon', 'Microsoft', 'Netflix', 'Uber']
            },
            {
                'id': 2,
                'title': 'Software Engineer',
                'category': 'Technology',
                'skills': ['Programming', 'Algorithms', 'System Design', 'Testing', 'Debugging',
                          'Java', 'Python', 'JavaScript', 'Cloud Computing', 'DevOps'],
                'personality_traits': ['INTJ', 'ISTJ', 'ENTJ', 'ESTJ', 'INTP'],
                'education_required': "Bachelor's in Computer Science",
                'experience_level': 'Entry to Senior',
                'salary_range': {'min': 70000, 'max': 200000, 'median': 110000},
                'job_growth': 22,
                'demand_score': 98,
                'remote_friendly': True,
                'stress_level': 'Medium',
                'description': 'Design, develop, and maintain software applications and systems',
                'day_to_day': ['Coding', 'Code reviews', 'System design', 'Bug fixing'],
                'companies': ['All major tech companies', 'Startups', 'Finance sector']
            },
            {
                'id': 3,
                'title': 'UX/UI Designer',
                'category': 'Design',
                'skills': ['User Research', 'Wireframing', 'Prototyping', 'UI Design', 'User Testing',
                          'Figma', 'Adobe XD', 'User Psychology', 'Interaction Design'],
                'personality_traits': ['ENFP', 'INFJ', 'INFP', 'ENFJ', 'ISFP'],
                'education_required': "Bachelor's in Design or related field",
                'experience_level': 'Entry to Senior',
                'salary_range': {'min': 60000, 'max': 130000, 'median': 85000},
                'job_growth': 18,
                'demand_score': 88,
                'remote_friendly': True,
                'stress_level': 'Medium',
                'description': 'Create user-centered designs for digital products and services',
                'day_to_day': ['User research', 'Creating prototypes', 'Design iterations', 'Team collaboration'],
                'companies': ['Tech companies', 'Design agencies', 'E-commerce']
            },
            {
                'id': 4,
                'title': 'Product Manager',
                'category': 'Business',
                'skills': ['Product Strategy', 'Market Research', 'Agile Methodology', 'Stakeholder Management',
                          'Data Analysis', 'Roadmapping', 'User Stories', 'Prioritization'],
                'personality_traits': ['ENTJ', 'ENFJ', 'ESTJ', 'ENTP', 'INTJ'],
                'education_required': "Bachelor's in Business or related field, often MBA",
                'experience_level': 'Mid to Senior',
                'salary_range': {'min': 80000, 'max': 180000, 'median': 125000},
                'job_growth': 20,
                'demand_score': 92,
                'remote_friendly': True,
                'stress_level': 'High',
                'description': 'Lead product development from conception to launch',
                'day_to_day': ['Strategy meetings', 'User research', 'Team coordination', 'Data analysis'],
                'companies': ['Tech companies', 'Startups', 'Large enterprises']
            },
            {
                'id': 5,
                'title': 'Digital Marketing Specialist',
                'category': 'Marketing',
                'skills': ['SEO', 'Content Marketing', 'Social Media', 'Google Analytics', 'Email Marketing',
                          'PPC Advertising', 'Conversion Optimization', 'Marketing Automation'],
                'personality_traits': ['ESFP', 'ENFP', 'ESTP', 'ENTP', 'ENFJ'],
                'education_required': "Bachelor's in Marketing or related field",
                'experience_level': 'Entry to Mid',
                'salary_range': {'min': 45000, 'max': 90000, 'median': 65000},
                'job_growth': 15,
                'demand_score': 85,
                'remote_friendly': True,
                'stress_level': 'Medium',
                'description': 'Develop and implement digital marketing strategies',
                'day_to_day': ['Campaign management', 'Content creation', 'Data analysis', 'Strategy planning'],
                'companies': ['Marketing agencies', 'E-commerce', 'All industries']
            }
        ]
    
    def load_personality_mapping(self):
        """Map personality types to career suitability scores"""
        return {
            'INTJ': {'analytical': 0.9, 'creative': 0.7, 'social': 0.3, 'practical': 0.8},
            'INTP': {'analytical': 0.9, 'creative': 0.8, 'social': 0.2, 'practical': 0.6},
            'ENTJ': {'analytical': 0.8, 'creative': 0.6, 'social': 0.8, 'practical': 0.9},
            'ENTP': {'analytical': 0.7, 'creative': 0.9, 'social': 0.7, 'practical': 0.6},
            'INFJ': {'analytical': 0.7, 'creative': 0.8, 'social': 0.8, 'practical': 0.5},
            'INFP': {'analytical': 0.6, 'creative': 0.9, 'social': 0.7, 'practical': 0.4},
            'ENFJ': {'analytical': 0.6, 'creative': 0.7, 'social': 0.9, 'practical': 0.7},
            'ENFP': {'analytical': 0.5, 'creative': 0.9, 'social': 0.8, 'practical': 0.5},
            'ISTJ': {'analytical': 0.8, 'creative': 0.4, 'social': 0.3, 'practical': 0.9},
            'ISFJ': {'analytical': 0.6, 'creative': 0.5, 'social': 0.7, 'practical': 0.8},
            'ESTJ': {'analytical': 0.7, 'creative': 0.4, 'social': 0.6, 'practical': 0.9},
            'ESFJ': {'analytical': 0.5, 'creative': 0.5, 'social': 0.9, 'practical': 0.8},
            'ISTP': {'analytical': 0.8, 'creative': 0.6, 'social': 0.3, 'practical': 0.9},
            'ISFP': {'analytical': 0.5, 'creative': 0.8, 'social': 0.6, 'practical': 0.7},
            'ESTP': {'analytical': 0.6, 'creative': 0.5, 'social': 0.8, 'practical': 0.9},
            'ESFP': {'analytical': 0.4, 'creative': 0.7, 'social': 0.9, 'practical': 0.8},
        }
    
    def load_industry_trends(self):
        """Current industry trends and future projections"""
        return {
            'Technology': {'growth': 25, 'remote_work': 85, 'salary_growth': 8},
            'Healthcare': {'growth': 18, 'remote_work': 30, 'salary_growth': 6},
            'Finance': {'growth': 12, 'remote_work': 60, 'salary_growth': 7},
            'Marketing': {'growth': 15, 'remote_work': 75, 'salary_growth': 5},
            'Design': {'growth': 20, 'remote_work': 80, 'salary_growth': 7},
            'Business': {'growth': 16, 'remote_work': 65, 'salary_growth': 6}
        }
    
    def calculate_personality_compatibility(self, user_personality, career_traits):
        """Advanced personality compatibility calculation"""
        if not user_personality or user_personality not in self.personality_mapping:
            return 0.5
        
        user_profile = self.personality_mapping[user_personality]
        
        # Calculate average compatibility with career's preferred personalities
        compatibilities = []
        for trait in career_traits:
            if trait in self.personality_mapping:
                career_profile = self.personality_mapping[trait]
                # Cosine similarity between personality vectors
                user_vec = np.array(list(user_profile.values()))
                career_vec = np.array(list(career_profile.values()))
                similarity = np.dot(user_vec, career_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(career_vec))
                compatibilities.append(similarity)
        
        return np.mean(compatibilities) if compatibilities else 0.5
    
    def calculate_skill_match(self, user_skills, required_skills):
        """Advanced skill matching using TF-IDF and semantic similarity"""
        if not user_skills or not required_skills:
            return 0.3  # Default low score
        
        # Convert to lists
        user_skill_list = [skill.strip().lower() for skill in user_skills.split(',')]
        required_skill_list = [skill.lower() for skill in required_skills]
        
        if not user_skill_list or not required_skill_list:
            return 0.3
        
        # Simple exact matching
        exact_matches = len(set(user_skill_list) & set(required_skill_list))
        exact_score = exact_matches / len(required_skill_list)
        
        # Partial matching (for similar skills)
        partial_matches = 0
        for req_skill in required_skill_list:
            for user_skill in user_skill_list:
                if user_skill in req_skill or req_skill in user_skill:
                    partial_matches += 1
                    break
        
        partial_score = partial_matches / len(required_skill_list)
        
        # Combined score (weighted towards exact matches)
        return (exact_score * 0.7 + partial_score * 0.3)
    
    def calculate_education_compatibility(self, user_education, required_education):
        """Calculate education level compatibility"""
        education_levels = {
            'high_school': 1,
            'undergraduate': 2,
            'graduate': 3,
            'phd': 4,
            'working': 2.5  # Professional experience counts
        }
        
        user_level = education_levels.get(user_education, 1)
        req_level = 2 if "Bachelor" in required_education else 3 if "Master" in required_education else 1
        
        if user_level >= req_level:
            return 1.0
        elif user_level >= req_level - 1:
            return 0.7
        else:
            return 0.3
    
    def calculate_market_factors(self, career, user_preferences):
        """Calculate market demand and trend factors"""
        industry = career['category']
        trends = self.industry_trends.get(industry, {'growth': 10, 'remote_work': 50, 'salary_growth': 3})
        
        market_score = 0.0
        
        # Job growth factor
        growth_factor = career['job_growth'] / 30  # Normalize to 0-1 scale
        market_score += growth_factor * 0.4
        
        # Remote work compatibility
        remote_preference = user_preferences.get('remote_work', 0.5)
        remote_score = (career['remote_friendly'] * remote_preference) * 0.3
        
        # Salary growth potential
        salary_growth = trends['salary_growth'] / 10  # Normalize
        market_score += salary_growth * 0.3
        
        return market_score + remote_score
    
    def generate_career_recommendations(self, user_data, top_n=10):
        """Generate comprehensive career recommendations"""
        recommendations = []
        
        for career in self.career_database:
            # Calculate various compatibility scores
            personality_score = self.calculate_personality_compatibility(
                user_data.get('personality_type'), 
                career['personality_traits']
            )
            
            skill_score = self.calculate_skill_match(
                user_data.get('skills', ''),
                career['skills']
            )
            
            education_score = self.calculate_education_compatibility(
                user_data.get('education_level', 'high_school'),
                career['education_required']
            )
            
            market_score = self.calculate_market_factors(
                career, 
                user_data.get('preferences', {})
            )
            
            # Weighted total score
            total_score = (
                personality_score * 0.25 +
                skill_score * 0.30 +
                education_score * 0.20 +
                market_score * 0.25
            )
            
            # Skill gap analysis
            user_skills = [skill.strip().lower() for skill in user_data.get('skills', '').split(',')] if user_data.get('skills') else []
            missing_skills = [
                skill for skill in career['skills'] 
                if not any(user_skill in skill.lower() for user_skill in user_skills)
            ][:5]  # Top 5 missing skills
            
            # Learning path suggestions
            learning_path = self.generate_learning_path(career, user_skills)
            
            recommendations.append({
                'career': career['title'],
                'category': career['category'],
                'match_score': round(total_score * 100, 1),
                'detailed_scores': {
                    'personality': round(personality_score * 100, 1),
                    'skills': round(skill_score * 100, 1),
                    'education': round(education_score * 100, 1),
                    'market': round(market_score * 100, 1)
                },
                'description': career['description'],
                'salary_range': career['salary_range'],
                'job_growth': career['job_growth'],
                'experience_level': career['experience_level'],
                'missing_skills': missing_skills,
                'learning_path': learning_path,
                'companies': career['companies'],
                'day_to_day': career['day_to_day'],
                'demand_score': career['demand_score'],
                'remote_friendly': career['remote_friendly']
            })
        
        # Sort by match score and return top N
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]
    
    def generate_learning_path(self, career, user_skills):
        """Generate personalized learning path to bridge skill gaps"""
        path = {
            'priority_skills': [],
            'recommended_courses': [],
            'timeline_estimate': '3-6 months',
            'resources': []
        }
        
        # Identify priority skills to learn
        for skill in career['skills'][:5]:  # Top 5 most important skills
            if not any(user_skill in skill.lower() for user_skill in user_skills):
                path['priority_skills'].append(skill)
        
        # Generate course recommendations based on missing skills
        course_mapping = {
            'Python': ['Python for Everybody (Coursera)', 'Automate the Boring Stuff with Python'],
            'Machine Learning': ['Machine Learning by Andrew Ng', 'Fast.ai Practical Deep Learning'],
            'Data Analysis': ['Google Data Analytics Professional Certificate'],
            'SQL': ['SQL for Data Science', 'The Complete SQL Bootcamp'],
            'JavaScript': ['JavaScript: The Complete Guide', 'The Modern JavaScript Tutorial'],
            'UX Design': ['Google UX Design Professional Certificate', 'Interaction Design Foundation'],
            'Product Management': ['Product Management Certified', 'Agile Methodology Fundamentals']
        }
        
        for skill in path['priority_skills'][:3]:
            if skill in course_mapping:
                path['recommended_courses'].extend(course_mapping[skill][:1])
        
        # Add general career resources
        path['resources'] = [
            f"{career['title']} Career Guide",
            "Industry networking events",
            "Professional certification programs"
        ]
        
        return path
    
    def analyze_career_clusters(self, user_data):
        """Cluster careers into categories for better insights"""
        recommendations = self.generate_career_recommendations(user_data, top_n=20)
        
        clusters = {}
        for rec in recommendations:
            category = rec['category']
            if category not in clusters:
                clusters[category] = []
            clusters[category].append(rec)
        
        return clusters

# Global instance
career_ai = AdvancedCareerAI()