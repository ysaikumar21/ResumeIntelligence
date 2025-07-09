"""
Database Manager Module
Handles SQLite database operations for storing resume and analysis data
Built for ATS Resume Analyzer - Data Science Portfolio Project
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
import streamlit as st
import os

class DatabaseManager:
    """Manages all database operations for the ATS Resume Analyzer"""
    
    def __init__(self, db_name="ats_analyzer.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create resumes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resumes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    raw_text TEXT,
                    extracted_data TEXT,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create job_descriptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT,
                    description TEXT NOT NULL,
                    required_skills TEXT,
                    experience_level TEXT,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create analysis_results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resume_id INTEGER,
                    job_description_id INTEGER,
                    ats_score INTEGER,
                    skill_match_score INTEGER,
                    keyword_match_score INTEGER,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    recommendations TEXT,
                    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (resume_id) REFERENCES resumes (id),
                    FOREIGN KEY (job_description_id) REFERENCES job_descriptions (id)
                )
            ''')
            
            # Create skill_tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    skill_name TEXT NOT NULL,
                    skill_category TEXT,
                    proficiency_level INTEGER,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            st.error(f"Database initialization error: {str(e)}")
    
    def create_user(self, name, email):
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (name, email) VALUES (?, ?)
            ''', (name, email))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return user_id
            
        except sqlite3.IntegrityError:
            # User already exists
            return self.get_user_by_email(email)['id']
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'created_at': user[3]
                }
            return None
            
        except Exception as e:
            st.error(f"Error fetching user: {str(e)}")
            return None
    
    def save_resume(self, user_id, filename, file_type, raw_text, extracted_data):
        """Save resume data to database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO resumes (user_id, filename, file_type, raw_text, extracted_data)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, filename, file_type, raw_text, json.dumps(extracted_data)))
            
            resume_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return resume_id
            
        except Exception as e:
            st.error(f"Error saving resume: {str(e)}")
            return None
    
    def get_user_resumes(self, user_id):
        """Get all resumes for a user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, filename, file_type, upload_date FROM resumes 
                WHERE user_id = ? ORDER BY upload_date DESC
            ''', (user_id,))
            
            resumes = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': resume[0],
                    'filename': resume[1],
                    'file_type': resume[2],
                    'upload_date': resume[3]
                }
                for resume in resumes
            ]
            
        except Exception as e:
            st.error(f"Error fetching resumes: {str(e)}")
            return []
    
    def save_job_description(self, title, company, description, required_skills, experience_level, location):
        """Save job description"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO job_descriptions (title, company, description, required_skills, experience_level, location)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, company, description, json.dumps(required_skills), experience_level, location))
            
            job_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return job_id
            
        except Exception as e:
            st.error(f"Error saving job description: {str(e)}")
            return None
    
    def save_analysis_result(self, resume_id, job_description_id, ats_score, skill_match_score, 
                           keyword_match_score, matched_skills, missing_skills, recommendations):
        """Save analysis results"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_results 
                (resume_id, job_description_id, ats_score, skill_match_score, keyword_match_score,
                 matched_skills, missing_skills, recommendations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (resume_id, job_description_id, ats_score, skill_match_score, keyword_match_score,
                  json.dumps(matched_skills), json.dumps(missing_skills), json.dumps(recommendations)))
            
            analysis_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return analysis_id
            
        except Exception as e:
            st.error(f"Error saving analysis result: {str(e)}")
            return None
    
    def get_analysis_history(self, user_id, limit=10):
        """Get analysis history for a user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT ar.*, r.filename, jd.title, jd.company 
                FROM analysis_results ar
                JOIN resumes r ON ar.resume_id = r.id
                JOIN job_descriptions jd ON ar.job_description_id = jd.id
                WHERE r.user_id = ?
                ORDER BY ar.analysis_date DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'analysis_id': result[0],
                    'ats_score': result[3],
                    'skill_match_score': result[4],
                    'keyword_match_score': result[5],
                    'analysis_date': result[9],
                    'resume_filename': result[10],
                    'job_title': result[11],
                    'company': result[12]
                }
                for result in results
            ]
            
        except Exception as e:
            st.error(f"Error fetching analysis history: {str(e)}")
            return []
    
    def update_skill_tracking(self, user_id, skill_name, skill_category, proficiency_level):
        """Update or insert skill tracking data"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Check if skill exists for user
            cursor.execute('''
                SELECT id FROM skill_tracking WHERE user_id = ? AND skill_name = ?
            ''', (user_id, skill_name))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing skill
                cursor.execute('''
                    UPDATE skill_tracking 
                    SET skill_category = ?, proficiency_level = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND skill_name = ?
                ''', (skill_category, proficiency_level, user_id, skill_name))
            else:
                # Insert new skill
                cursor.execute('''
                    INSERT INTO skill_tracking (user_id, skill_name, skill_category, proficiency_level)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, skill_name, skill_category, proficiency_level))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            st.error(f"Error updating skill tracking: {str(e)}")
            return False
    
    def get_user_skills(self, user_id):
        """Get all tracked skills for a user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT skill_name, skill_category, proficiency_level, last_updated
                FROM skill_tracking WHERE user_id = ?
                ORDER BY skill_category, skill_name
            ''', (user_id,))
            
            skills = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'skill_name': skill[0],
                    'skill_category': skill[1],
                    'proficiency_level': skill[2],
                    'last_updated': skill[3]
                }
                for skill in skills
            ]
            
        except Exception as e:
            st.error(f"Error fetching user skills: {str(e)}")
            return []
    
    def get_analytics_data(self, user_id):
        """Get comprehensive analytics data for dashboard"""
        try:
            conn = sqlite3.connect(self.db_name)
            
            # Get analysis trends
            trends_df = pd.read_sql_query('''
                SELECT ar.analysis_date, ar.ats_score, ar.skill_match_score, ar.keyword_match_score
                FROM analysis_results ar
                JOIN resumes r ON ar.resume_id = r.id
                WHERE r.user_id = ?
                ORDER BY ar.analysis_date
            ''', conn, params=(user_id,))
            
            # Get skill distribution
            skills_df = pd.read_sql_query('''
                SELECT skill_category, COUNT(*) as count, AVG(proficiency_level) as avg_proficiency
                FROM skill_tracking
                WHERE user_id = ?
                GROUP BY skill_category
            ''', conn, params=(user_id,))
            
            # Get recent analysis results
            recent_df = pd.read_sql_query('''
                SELECT ar.ats_score, jd.title, jd.company, ar.analysis_date
                FROM analysis_results ar
                JOIN resumes r ON ar.resume_id = r.id
                JOIN job_descriptions jd ON ar.job_description_id = jd.id
                WHERE r.user_id = ?
                ORDER BY ar.analysis_date DESC
                LIMIT 5
            ''', conn, params=(user_id,))
            
            conn.close()
            
            return {
                'trends': trends_df,
                'skills': skills_df,
                'recent': recent_df
            }
            
        except Exception as e:
            st.error(f"Error fetching analytics data: {str(e)}")
            return {'trends': pd.DataFrame(), 'skills': pd.DataFrame(), 'recent': pd.DataFrame()}
    
    def backup_database(self, backup_path="backup_ats_analyzer.db"):
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_name, backup_path)
            return True
        except Exception as e:
            st.error(f"Error creating backup: {str(e)}")
            return False