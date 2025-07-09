"""
Skill Matcher Module
Advanced skill matching and analysis for Data Science and IT roles
Provides intelligent skill gap analysis and career recommendations
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

class SkillMatcher:
    """Advanced skill matching and analysis system"""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        # Comprehensive skill database for Data Science and IT
        self.skill_database = {
            'programming_languages': {
                'beginner': ['Python', 'SQL', 'R', 'JavaScript', 'HTML', 'CSS'],
                'intermediate': ['Java', 'C++', 'Scala', 'Go', 'Ruby', 'PHP'],
                'advanced': ['Rust', 'Julia', 'Kotlin', 'Swift', 'C#', 'MATLAB']
            },
            'data_science_libraries': {
                'beginner': ['Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Plotly'],
                'intermediate': ['Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'OpenCV'],
                'advanced': ['JAX', 'Hugging Face', 'MLflow', 'Kubeflow', 'Apache Spark']
            },
            'machine_learning': {
                'beginner': ['Linear Regression', 'Logistic Regression', 'Decision Trees', 'K-Means'],
                'intermediate': ['Random Forest', 'SVM', 'Neural Networks', 'NLP', 'Computer Vision'],
                'advanced': ['Deep Learning', 'Reinforcement Learning', 'GANs', 'Transformer Models', 'MLOps']
            },
            'databases': {
                'beginner': ['MySQL', 'SQLite', 'PostgreSQL', 'Excel'],
                'intermediate': ['MongoDB', 'Redis', 'Cassandra', 'Neo4j'],
                'advanced': ['Elasticsearch', 'Apache Kafka', 'ClickHouse', 'Snowflake']
            },
            'cloud_platforms': {
                'beginner': ['AWS S3', 'Google Drive', 'Dropbox'],
                'intermediate': ['AWS EC2', 'Azure', 'Google Cloud Platform', 'Docker'],
                'advanced': ['Kubernetes', 'Apache Airflow', 'Terraform', 'Jenkins']
            },
            'data_visualization': {
                'beginner': ['Excel Charts', 'Google Sheets', 'Matplotlib', 'Seaborn'],
                'intermediate': ['Tableau', 'Power BI', 'Plotly', 'D3.js'],
                'advanced': ['Looker', 'Qlik Sense', 'Custom Dashboards', 'Real-time Viz']
            },
            'analytics_tools': {
                'beginner': ['Google Analytics', 'Excel Pivot Tables'],
                'intermediate': ['Jupyter Notebooks', 'RStudio', 'Databricks'],
                'advanced': ['Apache Zeppelin', 'MLflow', 'Weights & Biases']
            },
            'soft_skills': {
                'beginner': ['Communication', 'Teamwork', 'Problem Solving'],
                'intermediate': ['Project Management', 'Leadership', 'Presentation Skills'],
                'advanced': ['Strategic Thinking', 'Mentoring', 'Cross-functional Collaboration']
            }
        }
        
        # Job role skill requirements
        self.role_requirements = {
            'Data Scientist': {
                'core_skills': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Data Visualization'],
                'preferred_skills': ['R', 'TensorFlow', 'PyTorch', 'Tableau', 'AWS'],
                'experience_level': 'intermediate'
            },
            'Data Analyst': {
                'core_skills': ['SQL', 'Excel', 'Python', 'Data Visualization', 'Statistics'],
                'preferred_skills': ['Tableau', 'Power BI', 'R', 'Google Analytics'],
                'experience_level': 'beginner'
            },
            'Machine Learning Engineer': {
                'core_skills': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'MLOps'],
                'preferred_skills': ['Docker', 'Kubernetes', 'AWS', 'Apache Spark'],
                'experience_level': 'advanced'
            },
            'Data Engineer': {
                'core_skills': ['Python', 'SQL', 'Apache Spark', 'ETL', 'Cloud Platforms'],
                'preferred_skills': ['Kafka', 'Airflow', 'Docker', 'Kubernetes'],
                'experience_level': 'intermediate'
            },
            'Business Intelligence Analyst': {
                'core_skills': ['SQL', 'Tableau', 'Power BI', 'Excel', 'Data Modeling'],
                'preferred_skills': ['Python', 'R', 'DAX', 'ETL Tools'],
                'experience_level': 'beginner'
            },
            'Research Scientist': {
                'core_skills': ['Python', 'R', 'Statistics', 'Machine Learning', 'Research Methods'],
                'preferred_skills': ['Deep Learning', 'Publications', 'Mathematics', 'Domain Expertise'],
                'experience_level': 'advanced'
            }
        }
        
        # Skill synonyms and variations
        self.skill_synonyms = {
            'machine learning': ['ml', 'artificial intelligence', 'ai'],
            'python': ['python programming', 'python development'],
            'sql': ['structured query language', 'database queries'],
            'tensorflow': ['tf', 'tensor flow'],
            'pytorch': ['torch'],
            'data visualization': ['data viz', 'visualization', 'charting'],
            'amazon web services': ['aws'],
            'google cloud platform': ['gcp', 'google cloud'],
            'microsoft azure': ['azure'],
            'natural language processing': ['nlp'],
            'computer vision': ['cv', 'image processing']
        }
    
    def analyze_skill_match(self, resume_data, job_description):
        """Comprehensive skill matching analysis"""
        
        try:
            # Extract skills from resume and job description
            resume_skills = self._normalize_skills(resume_data.get('skills', []))
            job_skills = self._extract_job_skills(job_description)
            
            # Find matches and gaps
            matched_skills = self._find_skill_matches(resume_skills, job_skills)
            missing_skills = self._find_missing_skills(resume_skills, job_skills)
            
            # Calculate match percentage
            total_job_skills = len(job_skills)
            matched_count = len(matched_skills)
            match_percentage = (matched_count / max(1, total_job_skills)) * 100
            
            # Skill level analysis
            skill_levels = self._analyze_skill_levels(resume_skills)
            
            # Generate recommendations
            recommendations = self._generate_skill_recommendations(matched_skills, missing_skills, skill_levels)
            
            return {
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'match_percentage': round(match_percentage, 1),
                'total_job_skills': total_job_skills,
                'total_resume_skills': len(resume_skills),
                'skill_levels': skill_levels,
                'recommendations': recommendations
            }
            
        except Exception as e:
            st.error(f"Error in skill analysis: {str(e)}")
            return {
                'matched_skills': [],
                'missing_skills': [],
                'match_percentage': 0,
                'total_job_skills': 0,
                'total_resume_skills': 0,
                'skill_levels': {},
                'recommendations': []
            }
    
    def _normalize_skills(self, skills):
        """Normalize and clean skill names"""
        normalized = []
        
        for skill in skills:
            # Clean and normalize skill name
            clean_skill = re.sub(r'[^\w\s]', '', skill.lower().strip())
            
            # Check for synonyms
            for main_skill, synonyms in self.skill_synonyms.items():
                if clean_skill in synonyms or clean_skill == main_skill:
                    clean_skill = main_skill
                    break
            
            if len(clean_skill) > 1:  # Avoid single characters
                normalized.append(clean_skill)
        
        return list(set(normalized))  # Remove duplicates
    
    def _extract_job_skills(self, job_description):
        """Extract skills mentioned in job description"""
        job_text = job_description.lower()
        found_skills = []
        
        # Check all skills in database
        for category, levels in self.skill_database.items():
            for level, skills in levels.items():
                for skill in skills:
                    skill_lower = skill.lower()
                    # Check for exact matches or variations
                    if skill_lower in job_text or any(syn in job_text for syn in self.skill_synonyms.get(skill_lower, [])):
                        found_skills.append(skill_lower)
        
        # Extract additional technical terms
        tech_patterns = [
            r'\b(?:python|java|sql|r\b|javascript|html|css|c\+\+)\b',
            r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes)\b',
            r'\b(?:tableau|power\s*bi|excel|mysql|postgresql)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, job_text)
            found_skills.extend(matches)
        
        return list(set(found_skills))  # Remove duplicates
    
    def _find_skill_matches(self, resume_skills, job_skills):
        """Find matching skills between resume and job"""
        matches = []
        
        for job_skill in job_skills:
            for resume_skill in resume_skills:
                if (job_skill == resume_skill or 
                    job_skill in resume_skill or 
                    resume_skill in job_skill or
                    self._are_similar_skills(job_skill, resume_skill)):
                    matches.append(job_skill)
                    break
        
        return list(set(matches))
    
    def _find_missing_skills(self, resume_skills, job_skills):
        """Find skills mentioned in job but missing from resume"""
        missing = []
        
        for job_skill in job_skills:
            found = False
            for resume_skill in resume_skills:
                if (job_skill == resume_skill or 
                    job_skill in resume_skill or 
                    resume_skill in job_skill or
                    self._are_similar_skills(job_skill, resume_skill)):
                    found = True
                    break
            
            if not found:
                missing.append(job_skill)
        
        return missing
    
    def _are_similar_skills(self, skill1, skill2):
        """Check if two skills are similar using text similarity"""
        try:
            # Use simple string similarity for now
            longer = skill1 if len(skill1) > len(skill2) else skill2
            shorter = skill2 if len(skill1) > len(skill2) else skill1
            
            # If shorter skill is contained in longer skill with high overlap
            if len(shorter) > 3 and shorter in longer:
                return True
            
            # Check using character overlap
            overlap = len(set(skill1) & set(skill2))
            total_chars = len(set(skill1) | set(skill2))
            similarity = overlap / max(1, total_chars)
            
            return similarity > 0.7
            
        except:
            return False
    
    def _analyze_skill_levels(self, resume_skills):
        """Analyze skill levels based on skill database"""
        skill_levels = defaultdict(list)
        
        for skill in resume_skills:
            found_level = None
            for category, levels in self.skill_database.items():
                for level, skills_in_level in levels.items():
                    if any(skill in s.lower() or s.lower() in skill for s in skills_in_level):
                        found_level = level
                        break
                if found_level:
                    break
            
            if found_level:
                skill_levels[found_level].append(skill)
            else:
                skill_levels['unknown'].append(skill)
        
        return dict(skill_levels)
    
    def _generate_skill_recommendations(self, matched_skills, missing_skills, skill_levels):
        """Generate personalized skill development recommendations"""
        recommendations = []
        
        # Priority recommendations based on missing skills
        if missing_skills:
            high_priority = []
            medium_priority = []
            
            for skill in missing_skills[:5]:  # Top 5 missing skills
                # Check skill importance (beginner skills are higher priority)
                is_beginner_skill = False
                for category, levels in self.skill_database.items():
                    if skill in [s.lower() for s in levels.get('beginner', [])]:
                        is_beginner_skill = True
                        break
                
                if is_beginner_skill:
                    high_priority.append(skill)
                else:
                    medium_priority.append(skill)
            
            if high_priority:
                recommendations.append(f"🔥 High Priority: Learn {', '.join(high_priority[:3])}")
            
            if medium_priority:
                recommendations.append(f"📈 Medium Priority: Develop {', '.join(medium_priority[:3])}")
        
        # Skill level progression recommendations
        beginner_count = len(skill_levels.get('beginner', []))
        intermediate_count = len(skill_levels.get('intermediate', []))
        advanced_count = len(skill_levels.get('advanced', []))
        
        if beginner_count > intermediate_count * 2:
            recommendations.append("🎯 Focus on advancing from beginner to intermediate level skills")
        
        if intermediate_count > 5 and advanced_count < 2:
            recommendations.append("🚀 Ready to tackle advanced skills and specialized tools")
        
        # Career path recommendations
        recommendations.extend(self._get_career_path_recommendations(matched_skills, skill_levels))
        
        return recommendations
    
    def _get_career_path_recommendations(self, matched_skills, skill_levels):
        """Generate career path recommendations based on current skills"""
        recommendations = []
        
        # Analyze fit for different roles
        role_fits = {}
        for role, requirements in self.role_requirements.items():
            core_matches = len([s for s in requirements['core_skills'] if s.lower() in [ms.lower() for ms in matched_skills]])
            core_total = len(requirements['core_skills'])
            fit_percentage = (core_matches / core_total) * 100
            role_fits[role] = fit_percentage
        
        # Recommend best fitting roles
        best_roles = sorted(role_fits.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for role, fit in best_roles:
            if fit > 60:
                recommendations.append(f"💼 Strong fit for {role} ({fit:.0f}% skill match)")
            elif fit > 40:
                recommendations.append(f"📚 Potential fit for {role} - develop missing core skills")
        
        return recommendations
    
    def get_learning_path(self, target_role, current_skills):
        """Generate a learning path for a target role"""
        
        if target_role not in self.role_requirements:
            return None
        
        requirements = self.role_requirements[target_role]
        current_skills_lower = [s.lower() for s in current_skills]
        
        learning_path = {
            'role': target_role,
            'current_match': [],
            'missing_core': [],
            'missing_preferred': [],
            'learning_timeline': {},
            'resources': {}
        }
        
        # Analyze current skill match
        for skill in requirements['core_skills']:
            if skill.lower() in current_skills_lower:
                learning_path['current_match'].append(skill)
            else:
                learning_path['missing_core'].append(skill)
        
        for skill in requirements['preferred_skills']:
            if skill.lower() not in current_skills_lower:
                learning_path['missing_preferred'].append(skill)
        
        # Create learning timeline (simplified)
        timeline_weeks = 0
        for skill in learning_path['missing_core']:
            learning_path['learning_timeline'][skill] = f"Weeks {timeline_weeks + 1}-{timeline_weeks + 4}"
            timeline_weeks += 4
        
        for skill in learning_path['missing_preferred'][:3]:  # Top 3 preferred skills
            learning_path['learning_timeline'][skill] = f"Weeks {timeline_weeks + 1}-{timeline_weeks + 2}"
            timeline_weeks += 2
        
        return learning_path
    
    def analyze_market_trends(self, skills):
        """Analyze market trends for given skills (simplified simulation)"""
        
        # Simulated market data (in real app, this could connect to job market APIs)
        market_trends = {
            'python': {'demand': 95, 'trend': 'rising', 'avg_salary': 85000},
            'machine learning': {'demand': 90, 'trend': 'rising', 'avg_salary': 95000},
            'sql': {'demand': 85, 'trend': 'stable', 'avg_salary': 75000},
            'aws': {'demand': 88, 'trend': 'rising', 'avg_salary': 90000},
            'tableau': {'demand': 80, 'trend': 'stable', 'avg_salary': 80000},
            'tensorflow': {'demand': 85, 'trend': 'rising', 'avg_salary': 100000},
            'r': {'demand': 70, 'trend': 'declining', 'avg_salary': 78000},
            'excel': {'demand': 75, 'trend': 'stable', 'avg_salary': 65000}
        }
        
        skill_analysis = {}
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in market_trends:
                skill_analysis[skill] = market_trends[skill_lower]
            else:
                # Default values for unknown skills
                skill_analysis[skill] = {
                    'demand': 60, 
                    'trend': 'stable', 
                    'avg_salary': 70000
                }
        
        return skill_analysis