"""
ATS Resume Analyzer - Python Version
Built for Data Science Students & Fresher IT Roles
Author: For Saikumar Yaramala - B.Tech Electronics and Data Science
"""

import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

# Import custom modules
from utils.resume_parser import ResumeParser
from utils.database_manager import DatabaseManager
from utils.ats_analyzer import ATSAnalyzer
from utils.skill_matcher import SkillMatcher

# Page configuration
st.set_page_config(
    page_title="ATS Resume Analyzer - Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Bootstrap-style components
def load_css():
    st.markdown("""
    <style>
    /* Bootstrap-inspired styling */
    .main-header {
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 123, 255, 0.1);
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #007bff;
    }
    
    .success-card {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-card {
        background: #cce7ff;
        border-left: 4px solid #007bff;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .metric-container {
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .skill-tag {
        background: #007bff;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .missing-skill-tag {
        background: #dc3545;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .btn-primary {
        background: #007bff;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 5px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        background: #0056b3;
        transform: translateY(-1px);
    }
    
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        transition: width 0.5s ease;
    }
    
    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    }
    
    .recommendation-item {
        background: #fff;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
    }
    
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 ATS Resume Analyzer</h1>
        <p>Professional Resume Analysis for Data Science & IT Professionals</p>
        <p><em>Built for Saikumar Yaramala - B.Tech Electronics & Data Science</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div class="sidebar-info">
        <h3>📊 Portfolio Project</h3>
        <p><strong>Developer:</strong> Saikumar Yaramala</p>
        <p><strong>Field:</strong> Data Science & Electronics</p>
        <p><strong>Target:</strong> Fresher IT Roles</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu_options = ["🏠 Home", "📄 Resume Analysis", "📊 Analytics Dashboard", "💼 Job Matching", "🎯 Skill Recommendations"]
    selected_menu = st.sidebar.selectbox("Navigation", menu_options)
    
    # Main content based on selection
    if selected_menu == "🏠 Home":
        show_home_page()
    elif selected_menu == "📄 Resume Analysis":
        show_resume_analysis()
    elif selected_menu == "📊 Analytics Dashboard":
        show_analytics_dashboard()
    elif selected_menu == "💼 Job Matching":
        show_job_matching()
    elif selected_menu == "🎯 Skill Recommendations":
        show_skill_recommendations()

def show_home_page():
    st.markdown("""
    <div class="card">
        <h2>Welcome to Professional ATS Resume Analyzer</h2>
        <p>This application helps Data Science and IT professionals optimize their resumes for Applicant Tracking Systems (ATS).</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3>📊 Smart Analysis</h3>
            <p>Advanced algorithms analyze your resume against job requirements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3>🎯 ATS Optimization</h3>
            <p>Get specific recommendations to improve ATS compatibility</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3>💼 Job Matching</h3>
            <p>Match your skills with Data Science and IT job requirements</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("""
    <div class="info-card">
        <h3>🚀 Quick Start Guide</h3>
        <ol>
            <li><strong>Upload Resume:</strong> Go to Resume Analysis and upload your PDF/DOCX file</li>
            <li><strong>Add Job Description:</strong> Paste the target job description</li>
            <li><strong>Get Analysis:</strong> Receive detailed ATS score and recommendations</li>
            <li><strong>View Analytics:</strong> Check comprehensive skill analysis and improvements</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

def show_resume_analysis():
    st.markdown("""
    <div class="card">
        <h2>📄 Resume Analysis & ATS Scoring</h2>
        <p>Upload your resume and get detailed ATS compatibility analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose your resume file", 
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files"
    )
    
    if uploaded_file is not None:
        # Process the uploaded file
        parser = ResumeParser()
        
        with st.spinner("Extracting resume content..."):
            resume_data = parser.extract_resume_data(uploaded_file)
        
        if resume_data:
            st.markdown("""
            <div class="success-card">
                <h4>✅ Resume Successfully Processed!</h4>
                <p>Resume content has been extracted and analyzed.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display extracted information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 👤 Personal Information")
                st.write(f"**Name:** {resume_data.get('name', 'Not found')}")
                st.write(f"**Email:** {resume_data.get('email', 'Not found')}")
                st.write(f"**Phone:** {resume_data.get('phone', 'Not found')}")
                
                st.markdown("### 🎓 Education")
                education = resume_data.get('education', [])
                if education:
                    for edu in education:
                        st.write(f"• {edu}")
                else:
                    st.write("Education information not clearly identified")
            
            with col2:
                st.markdown("### 💻 Technical Skills")
                skills = resume_data.get('skills', [])
                if skills:
                    skills_html = ""
                    for skill in skills:
                        skills_html += f'<span class="skill-tag">{skill}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.write("Skills not clearly identified")
                
                st.markdown("### 💼 Experience")
                experience = resume_data.get('experience', [])
                if experience:
                    for exp in experience:
                        st.write(f"• {exp}")
                else:
                    st.write("Experience information not clearly identified")
            
            # Job description input
            st.markdown("### 🎯 Job Description Analysis")
            job_description = st.text_area(
                "Paste the target job description",
                height=200,
                placeholder="Paste the complete job description here for analysis..."
            )
            
            if job_description and st.button("🔍 Analyze Resume vs Job"):
                analyze_resume_job_match(resume_data, job_description)

def analyze_resume_job_match(resume_data, job_description):
    """Analyze how well the resume matches the job description"""
    
    analyzer = ATSAnalyzer()
    matcher = SkillMatcher()
    
    with st.spinner("Analyzing resume against job requirements..."):
        # Perform ATS analysis
        ats_score = analyzer.calculate_ats_score(resume_data, job_description)
        skill_analysis = matcher.analyze_skill_match(resume_data, job_description)
    
    # Display results
    st.markdown("## 📊 Analysis Results")
    
    # ATS Score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score_color = "success" if ats_score >= 70 else "warning" if ats_score >= 50 else "danger"
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="color: {'#28a745' if ats_score >= 70 else '#ffc107' if ats_score >= 50 else '#dc3545'}">{ats_score}%</h2>
            <p><strong>Overall ATS Score</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        skill_match_pct = skill_analysis['match_percentage']
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="color: {'#28a745' if skill_match_pct >= 70 else '#ffc107' if skill_match_pct >= 50 else '#dc3545'}">{skill_match_pct}%</h2>
            <p><strong>Skill Match</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        keyword_score = analyzer.calculate_keyword_score(resume_data, job_description)
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="color: {'#28a745' if keyword_score >= 70 else '#ffc107' if keyword_score >= 50 else '#dc3545'}">{keyword_score}%</h2>
            <p><strong>Keyword Match</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Skill Analysis
    st.markdown("### 🎯 Skill Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Matched Skills")
        matched_skills = skill_analysis['matched_skills']
        if matched_skills:
            skills_html = ""
            for skill in matched_skills:
                skills_html += f'<span class="skill-tag">{skill}</span>'
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.write("No matched skills found")
    
    with col2:
        st.markdown("#### ❌ Missing Skills")
        missing_skills = skill_analysis['missing_skills']
        if missing_skills:
            skills_html = ""
            for skill in missing_skills:
                skills_html += f'<span class="missing-skill-tag">{skill}</span>'
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.write("Great! All required skills are present")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    recommendations = analyzer.get_recommendations(ats_score, skill_analysis, keyword_score)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="recommendation-item">
            <strong>{i}.</strong> {rec}
        </div>
        """, unsafe_allow_html=True)

def show_analytics_dashboard():
    st.markdown("""
    <div class="card">
        <h2>📊 Analytics Dashboard</h2>
        <p>Comprehensive analytics and insights for your resume optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample analytics data (in real app, this would come from database)
    create_sample_analytics()

def create_sample_analytics():
    """Create sample analytics visualizations"""
    
    # Sample data for demonstration
    skill_categories = ['Python', 'Data Analysis', 'Machine Learning', 'SQL', 'Visualization', 'Statistics']
    current_scores = [85, 75, 60, 90, 70, 65]
    target_scores = [90, 85, 80, 95, 85, 80]
    
    # Skill comparison chart
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Current Level', x=skill_categories, y=current_scores, marker_color='#007bff'))
    fig.add_trace(go.Bar(name='Target Level', x=skill_categories, y=target_scores, marker_color='#28a745'))
    
    fig.update_layout(
        title='Skill Level Analysis - Data Science Profile',
        xaxis_title='Skills',
        yaxis_title='Proficiency Score',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress indicators
    st.markdown("### 📈 Skill Development Progress")
    
    for skill, current, target in zip(skill_categories, current_scores, target_scores):
        progress = (current / target) * 100
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            st.write(f"**{skill}**")
        
        with col2:
            st.progress(progress / 100)
        
        with col3:
            st.write(f"{current}/{target}")

def show_job_matching():
    st.markdown("""
    <div class="card">
        <h2>💼 Job Matching for Data Science Roles</h2>
        <p>Find the best matching jobs based on your current skill set</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample job data
    jobs_data = [
        {
            "title": "Junior Data Scientist",
            "company": "Tech Startup Inc.",
            "match_score": 85,
            "required_skills": ["Python", "Pandas", "Machine Learning", "SQL"],
            "location": "Hyderabad",
            "experience": "0-1 years"
        },
        {
            "title": "Data Analyst",
            "company": "Analytics Corp",
            "match_score": 92,
            "required_skills": ["Python", "SQL", "Tableau", "Statistics"],
            "location": "Bangalore", 
            "experience": "Fresher"
        },
        {
            "title": "ML Engineer Intern",
            "company": "AI Solutions Ltd",
            "match_score": 78,
            "required_skills": ["Python", "TensorFlow", "Machine Learning", "Git"],
            "location": "Chennai",
            "experience": "Internship"
        }
    ]
    
    for job in jobs_data:
        create_job_card(job)

def create_job_card(job):
    """Create a job card with match information"""
    
    match_color = "#28a745" if job['match_score'] >= 80 else "#ffc107" if job['match_score'] >= 60 else "#dc3545"
    
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3>{job['title']}</h3>
                <p><strong>{job['company']}</strong> • {job['location']} • {job['experience']}</p>
            </div>
            <div style="text-align: center;">
                <h2 style="color: {match_color}; margin: 0;">{job['match_score']}%</h2>
                <p style="margin: 0;"><strong>Match Score</strong></p>
            </div>
        </div>
        <p><strong>Required Skills:</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills display
    skills_html = ""
    for skill in job['required_skills']:
        skills_html += f'<span class="skill-tag">{skill}</span>'
    st.markdown(skills_html, unsafe_allow_html=True)
    
    st.markdown("---")

def show_skill_recommendations():
    st.markdown("""
    <div class="card">
        <h2>🎯 Personalized Skill Recommendations</h2>
        <p>Tailored recommendations for Data Science and IT career growth</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Skill categories for Data Science
    categories = {
        "Programming Languages": {
            "current": ["Python", "SQL"],
            "recommended": ["R", "Scala", "Java"],
            "priority": "High"
        },
        "Machine Learning": {
            "current": ["Scikit-learn", "Pandas"],
            "recommended": ["TensorFlow", "PyTorch", "Keras"],
            "priority": "High"
        },
        "Data Visualization": {
            "current": ["Matplotlib"],
            "recommended": ["Tableau", "Power BI", "Plotly"],
            "priority": "Medium"
        },
        "Cloud Platforms": {
            "current": [],
            "recommended": ["AWS", "Azure", "Google Cloud"],
            "priority": "Medium"
        },
        "Big Data Tools": {
            "current": [],
            "recommended": ["Spark", "Hadoop", "Kafka"],
            "priority": "Low"
        }
    }
    
    for category, data in categories.items():
        create_skill_category_card(category, data)

def create_skill_category_card(category, data):
    """Create skill category recommendation card"""
    
    priority_colors = {
        "High": "#dc3545",
        "Medium": "#ffc107", 
        "Low": "#28a745"
    }
    
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3>{category}</h3>
            <span style="background: {priority_colors[data['priority']]}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                {data['priority']} Priority
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Current Skills:**")
        if data['current']:
            for skill in data['current']:
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("None identified")
    
    with col2:
        st.markdown("**🎯 Recommended to Learn:**")
        for skill in data['recommended']:
            st.markdown(f'<span class="missing-skill-tag">{skill}</span>', unsafe_allow_html=True)
    
    st.markdown("---")

if __name__ == "__main__":
    main()