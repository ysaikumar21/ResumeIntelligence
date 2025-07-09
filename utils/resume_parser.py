"""
Resume Parser Module
Extracts and processes resume content from PDF, DOCX, and TXT files
Built for Data Science and IT professional resume analysis
"""

import re
import io
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeParser:
    """Advanced resume parser for extracting structured data from resumes"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # Data Science and IT skill keywords
        self.technical_skills = {
            'programming_languages': [
                'python', 'r', 'java', 'scala', 'sql', 'javascript', 'c++', 'c#', 
                'matlab', 'sas', 'spss', 'julia', 'go', 'rust', 'kotlin'
            ],
            'data_science_tools': [
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'matplotlib', 'seaborn', 'plotly', 'bokeh', 'jupyter', 'anaconda',
                'spyder', 'rstudio', 'tableau', 'power bi', 'qlik'
            ],
            'machine_learning': [
                'machine learning', 'deep learning', 'neural networks', 'nlp',
                'computer vision', 'reinforcement learning', 'supervised learning',
                'unsupervised learning', 'regression', 'classification', 'clustering',
                'random forest', 'svm', 'decision trees', 'gradient boosting'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'cassandra', 'redis', 'elasticsearch',
                'oracle', 'sql server', 'sqlite', 'hive', 'spark sql'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes',
                'apache spark', 'hadoop', 'kafka', 'airflow', 'jenkins'
            ],
            'analytics_tools': [
                'excel', 'google analytics', 'mixpanel', 'segment', 'looker',
                'databricks', 'snowflake', 'redshift', 'bigquery'
            ]
        }
        
        # Education keywords
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'university', 'college',
            'b.tech', 'm.tech', 'b.sc', 'm.sc', 'mba', 'diploma', 'certification'
        ]
        
        # Experience keywords
        self.experience_keywords = [
            'experience', 'worked', 'internship', 'project', 'developed',
            'analyzed', 'implemented', 'designed', 'built', 'created'
        ]
    
    def extract_resume_data(self, uploaded_file):
        """Main method to extract data from uploaded resume file"""
        
        try:
            # Extract text based on file type
            if uploaded_file.type == "application/pdf":
                text = self._extract_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = self._extract_from_docx(uploaded_file)
            elif uploaded_file.type == "text/plain":
                text = self._extract_from_txt(uploaded_file)
            else:
                st.error("Unsupported file format")
                return None
            
            if not text:
                st.error("Could not extract text from the file")
                return None
            
            # Process and structure the extracted text
            resume_data = self._process_resume_text(text)
            return resume_data
            
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")
            return None
    
    def _extract_from_pdf(self, uploaded_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def _extract_from_docx(self, uploaded_file):
        """Extract text from DOCX file"""
        try:
            doc = Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def _extract_from_txt(self, uploaded_file):
        """Extract text from TXT file"""
        try:
            return uploaded_file.read().decode('utf-8')
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
    
    def _process_resume_text(self, text):
        """Process and extract structured information from resume text"""
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        resume_data = {
            'raw_text': text,
            'name': self._extract_name(lines),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'skills': self._extract_skills(text_lower),
            'education': self._extract_education(lines),
            'experience': self._extract_experience(lines),
            'certifications': self._extract_certifications(lines),
            'projects': self._extract_projects(lines)
        }
        
        return resume_data
    
    def _extract_name(self, lines):
        """Extract name from resume (usually in first few lines)"""
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 0 and len(line.split()) >= 2 and len(line.split()) <= 4:
                # Check if line looks like a name (contains only letters and spaces)
                if re.match(r'^[A-Za-z\s\.]+$', line) and '@' not in line and not any(char.isdigit() for char in line):
                    return line.title()
        return "Name not found"
    
    def _extract_email(self, text):
        """Extract email address using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "Email not found"
    
    def _extract_phone(self, text):
        """Extract phone number using regex"""
        phone_patterns = [
            r'(\+\d{1,3}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'(\+\d{1,3}\s?)?\d{10}',
            r'(\+\d{1,3}\s?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
        
        return "Phone not found"
    
    def _extract_skills(self, text_lower):
        """Extract technical skills from resume text"""
        found_skills = []
        
        for category, skills_list in self.technical_skills.items():
            for skill in skills_list:
                if skill.lower() in text_lower:
                    found_skills.append(skill.title())
        
        # Remove duplicates and return unique skills
        return list(set(found_skills))
    
    def _extract_education(self, lines):
        """Extract education information"""
        education_info = []
        education_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if we're in education section
            if any(keyword in line_lower for keyword in ['education', 'qualification', 'academic']):
                education_section = True
                continue
            
            # Stop if we hit another section
            if education_section and any(keyword in line_lower for keyword in ['experience', 'skill', 'project', 'certification']):
                break
            
            # Extract education entries
            if education_section and line.strip():
                if any(keyword in line_lower for keyword in self.education_keywords):
                    education_info.append(line.strip())
        
        return education_info if education_info else ["Education information not clearly identified"]
    
    def _extract_experience(self, lines):
        """Extract work experience information"""
        experience_info = []
        experience_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if we're in experience section
            if any(keyword in line_lower for keyword in ['experience', 'employment', 'work history', 'career']):
                experience_section = True
                continue
            
            # Stop if we hit another section
            if experience_section and any(keyword in line_lower for keyword in ['education', 'skill', 'project', 'certification']):
                break
            
            # Extract experience entries
            if experience_section and line.strip():
                if any(keyword in line_lower for keyword in self.experience_keywords) or len(line.strip()) > 20:
                    experience_info.append(line.strip())
        
        return experience_info if experience_info else ["Experience information not clearly identified"]
    
    def _extract_certifications(self, lines):
        """Extract certifications information"""
        cert_info = []
        cert_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in ['certification', 'certificate', 'license']):
                cert_section = True
                if line.strip() and not any(keyword in line_lower for keyword in ['certification', 'certificate']):
                    cert_info.append(line.strip())
                continue
            
            if cert_section and any(keyword in line_lower for keyword in ['education', 'experience', 'skill', 'project']):
                break
            
            if cert_section and line.strip():
                cert_info.append(line.strip())
        
        return cert_info if cert_info else ["No certifications found"]
    
    def _extract_projects(self, lines):
        """Extract project information"""
        project_info = []
        project_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in ['project', 'portfolio']):
                project_section = True
                continue
            
            if project_section and any(keyword in line_lower for keyword in ['education', 'experience', 'skill', 'certification']):
                break
            
            if project_section and line.strip() and len(line.strip()) > 10:
                project_info.append(line.strip())
        
        return project_info if project_info else ["No projects clearly identified"]