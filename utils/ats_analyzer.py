"""
ATS Analyzer Module
Analyzes resume compatibility with Applicant Tracking Systems
Specialized for Data Science and IT job applications
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

class ATSAnalyzer:
    """Advanced ATS compatibility analyzer for resumes"""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        # ATS-friendly formatting patterns
        self.ats_patterns = {
            'good_formats': [
                r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # Proper names
                r'\d{4}-\d{4}',  # Date ranges
                r'\b\d{1,2}/\d{4}\b',  # Month/Year
                r'\b[A-Z]+\b',  # Acronyms
            ],
            'bad_formats': [
                r'[^\w\s-]',  # Special characters (excluding hyphens)
                r'\t',  # Tabs
                r'\s{3,}',  # Multiple spaces
            ]
        }
        
        # Data Science and IT specific keywords
        self.domain_keywords = {
            'data_science': [
                'data science', 'machine learning', 'artificial intelligence', 'deep learning',
                'data analysis', 'statistical analysis', 'predictive modeling', 'data mining',
                'big data', 'analytics', 'visualization', 'python', 'r', 'sql', 'tableau',
                'power bi', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'
            ],
            'software_engineering': [
                'software development', 'programming', 'coding', 'algorithms', 'data structures',
                'object-oriented programming', 'agile', 'scrum', 'version control', 'git',
                'testing', 'debugging', 'api', 'database', 'framework', 'libraries'
            ],
            'general_it': [
                'information technology', 'technical skills', 'problem solving',
                'troubleshooting', 'system administration', 'network', 'security',
                'cloud computing', 'aws', 'azure', 'devops', 'automation'
            ]
        }
        
        # ATS scoring weights
        self.scoring_weights = {
            'keyword_match': 0.35,
            'skill_match': 0.25,
            'format_quality': 0.15,
            'content_structure': 0.15,
            'domain_relevance': 0.10
        }
    
    def calculate_ats_score(self, resume_data, job_description):
        """Calculate comprehensive ATS compatibility score"""
        
        try:
            # Calculate individual scores
            keyword_score = self.calculate_keyword_score(resume_data, job_description)
            skill_score = self.calculate_skill_match_score(resume_data, job_description)
            format_score = self.calculate_format_score(resume_data['raw_text'])
            structure_score = self.calculate_structure_score(resume_data)
            domain_score = self.calculate_domain_relevance(resume_data, job_description)
            
            # Calculate weighted total score
            total_score = (
                keyword_score * self.scoring_weights['keyword_match'] +
                skill_score * self.scoring_weights['skill_match'] +
                format_score * self.scoring_weights['format_quality'] +
                structure_score * self.scoring_weights['content_structure'] +
                domain_score * self.scoring_weights['domain_relevance']
            )
            
            return round(total_score)
            
        except Exception as e:
            st.error(f"Error calculating ATS score: {str(e)}")
            return 50  # Default middle score
    
    def calculate_keyword_score(self, resume_data, job_description):
        """Calculate keyword matching score using TF-IDF similarity"""
        
        try:
            resume_text = resume_data['raw_text'].lower()
            job_text = job_description.lower()
            
            # Use TF-IDF to find similarity
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            score = similarity * 100
            
            return min(100, max(0, score))
            
        except Exception as e:
            st.error(f"Error calculating keyword score: {str(e)}")
            return 50
    
    def calculate_skill_match_score(self, resume_data, job_description):
        """Calculate how well resume skills match job requirements"""
        
        try:
            resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
            job_text = job_description.lower()
            
            # Extract skills mentioned in job description
            job_skills = []
            all_skills = []
            
            # Collect all known skills
            for category in ['programming_languages', 'data_science_tools', 'machine_learning', 
                           'databases', 'cloud_platforms', 'analytics_tools']:
                if hasattr(self, 'technical_skills') and category in self.technical_skills:
                    all_skills.extend(self.technical_skills[category])
            
            # Add domain keywords as potential skills
            for domain, keywords in self.domain_keywords.items():
                all_skills.extend(keywords)
            
            # Add more technical skills
            technical_skills_list = [
                'python', 'java', 'javascript', 'sql', 'r', 'scala', 'c++', 'c#',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi', 'excel',
                'mysql', 'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'docker'
            ]
            all_skills.extend(technical_skills_list)
            
            # Find skills mentioned in job description
            for skill in all_skills:
                if skill.lower() in job_text:
                    job_skills.append(skill.lower())
            
            if not job_skills:
                return 75  # If no specific skills found, give moderate score
            
            # Calculate match percentage
            matched_skills = set(resume_skills) & set(job_skills)
            match_percentage = (len(matched_skills) / len(job_skills)) * 100
            
            return min(100, max(0, match_percentage))
            
        except Exception as e:
            st.error(f"Error calculating skill match score: {str(e)}")
            return 50
    
    def calculate_format_score(self, resume_text):
        """Calculate ATS-friendly formatting score"""
        
        try:
            score = 100
            
            # Check for bad formatting patterns
            for pattern in self.ats_patterns['bad_formats']:
                matches = len(re.findall(pattern, resume_text))
                score -= min(20, matches * 2)  # Deduct points for bad formatting
            
            # Check for good formatting patterns
            good_patterns_found = 0
            for pattern in self.ats_patterns['good_formats']:
                if re.search(pattern, resume_text):
                    good_patterns_found += 1
            
            # Bonus for good formatting
            if good_patterns_found >= 2:
                score += 10
            
            return max(0, min(100, score))
            
        except Exception as e:
            st.error(f"Error calculating format score: {str(e)}")
            return 75
    
    def calculate_structure_score(self, resume_data):
        """Calculate score based on resume structure and completeness"""
        
        try:
            score = 0
            max_score = 100
            
            # Check for essential sections
            section_scores = {
                'name': 15 if resume_data.get('name') and resume_data['name'] != "Name not found" else 0,
                'email': 15 if resume_data.get('email') and '@' in resume_data['email'] else 0,
                'phone': 10 if resume_data.get('phone') and resume_data['phone'] != "Phone not found" else 0,
                'skills': 25 if resume_data.get('skills') and len(resume_data['skills']) > 0 else 0,
                'experience': 20 if resume_data.get('experience') and len(resume_data['experience']) > 0 else 0,
                'education': 15 if resume_data.get('education') and len(resume_data['education']) > 0 else 0
            }
            
            score = sum(section_scores.values())
            
            return min(100, max(0, score))
            
        except Exception as e:
            st.error(f"Error calculating structure score: {str(e)}")
            return 50
    
    def calculate_domain_relevance(self, resume_data, job_description):
        """Calculate how relevant the resume is to the target domain"""
        
        try:
            resume_text = resume_data['raw_text'].lower()
            job_text = job_description.lower()
            
            # Determine job domain
            job_domain = self._identify_job_domain(job_text)
            
            # Count domain-relevant keywords in resume
            relevant_keywords = self.domain_keywords.get(job_domain, [])
            found_keywords = 0
            
            for keyword in relevant_keywords:
                if keyword.lower() in resume_text:
                    found_keywords += 1
            
            # Calculate relevance score
            if relevant_keywords:
                relevance_score = (found_keywords / len(relevant_keywords)) * 100
            else:
                relevance_score = 75  # Default score if no specific domain identified
            
            return min(100, max(0, relevance_score))
            
        except Exception as e:
            st.error(f"Error calculating domain relevance: {str(e)}")
            return 50
    
    def _identify_job_domain(self, job_text):
        """Identify the primary domain of the job"""
        
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in job_text:
                    score += 1
            domain_scores[domain] = score
        
        # Return domain with highest score
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        else:
            return 'general_it'  # Default domain
    
    def get_recommendations(self, ats_score, skill_analysis, keyword_score):
        """Generate specific recommendations for improving ATS score"""
        
        recommendations = []
        
        try:
            # Score-based recommendations
            if ats_score < 70:
                recommendations.append("🎯 Overall ATS score needs improvement. Focus on keyword optimization and formatting.")
            
            if keyword_score < 60:
                recommendations.append("📝 Include more relevant keywords from the job description in your resume.")
                recommendations.append("💡 Mirror the language used in the job posting while staying truthful.")
            
            if skill_analysis['match_percentage'] < 70:
                recommendations.append("🔧 Highlight transferable skills that relate to job requirements.")
                recommendations.append("📚 Consider learning missing critical skills mentioned in the job description.")
            
            # Missing skills recommendations
            missing_skills = skill_analysis.get('missing_skills', [])
            if missing_skills:
                top_missing = missing_skills[:3]  # Top 3 missing skills
                recommendations.append(f"🎓 Priority skills to learn: {', '.join(top_missing)}")
            
            # Formatting recommendations
            if ats_score < 80:
                recommendations.extend([
                    "📄 Use standard section headings (Experience, Education, Skills, etc.)",
                    "🔤 Use standard fonts and avoid special characters or graphics",
                    "📱 Ensure consistent formatting and proper spacing",
                    "📊 Use bullet points for achievements and responsibilities"
                ])
            
            # Data Science specific recommendations
            recommendations.extend([
                "📊 Include quantifiable achievements (e.g., 'Improved model accuracy by 15%')",
                "🔬 Mention specific tools, libraries, and technologies you've used",
                "📈 Highlight projects with measurable business impact",
                "🎯 Tailor your resume for each specific job application"
            ])
            
            # If score is already good
            if ats_score >= 85:
                recommendations = [
                    "✅ Excellent ATS compatibility! Your resume is well-optimized.",
                    "🌟 Continue to tailor keywords for each specific job application",
                    "📈 Keep your skills section updated with latest technologies"
                ]
            
            return recommendations[:8]  # Limit to top 8 recommendations
            
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return ["Unable to generate recommendations. Please try again."]
    
    def analyze_keyword_density(self, resume_text, job_description):
        """Analyze keyword density and frequency"""
        
        try:
            # Extract important keywords from job description
            job_words = word_tokenize(job_description.lower())
            job_words = [word for word in job_words if word.isalpha() and word not in self.stop_words]
            
            # Get word frequency from job description
            job_word_freq = Counter(job_words)
            
            # Extract words from resume
            resume_words = word_tokenize(resume_text.lower())
            resume_words = [word for word in resume_words if word.isalpha() and word not in self.stop_words]
            resume_word_freq = Counter(resume_words)
            
            # Find keyword matches and calculate density
            keyword_analysis = {}
            
            # Analyze top keywords from job description
            for word, job_freq in job_word_freq.most_common(20):
                if len(word) > 3:  # Focus on meaningful words
                    resume_freq = resume_word_freq.get(word, 0)
                    keyword_analysis[word] = {
                        'job_frequency': job_freq,
                        'resume_frequency': resume_freq,
                        'density_score': min(100, (resume_freq / max(1, job_freq)) * 100)
                    }
            
            return keyword_analysis
            
        except Exception as e:
            st.error(f"Error analyzing keyword density: {str(e)}")
            return {}
    
    def generate_ats_report(self, resume_data, job_description):
        """Generate comprehensive ATS analysis report"""
        
        try:
            # Calculate all scores
            ats_score = self.calculate_ats_score(resume_data, job_description)
            keyword_score = self.calculate_keyword_score(resume_data, job_description)
            format_score = self.calculate_format_score(resume_data['raw_text'])
            structure_score = self.calculate_structure_score(resume_data)
            
            # Analyze keywords
            keyword_analysis = self.analyze_keyword_density(resume_data['raw_text'], job_description)
            
            # Generate report
            report = {
                'overall_score': ats_score,
                'component_scores': {
                    'keyword_match': keyword_score,
                    'format_quality': format_score,
                    'content_structure': structure_score
                },
                'keyword_analysis': keyword_analysis,
                'recommendations': self.get_recommendations(ats_score, {'match_percentage': keyword_score}, keyword_score),
                'analysis_date': str(np.datetime64('now'))
            }
            
            return report
            
        except Exception as e:
            st.error(f"Error generating ATS report: {str(e)}")
            return None