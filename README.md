# ATS Resume Analyzer - Python Portfolio Project

# 🧠 Resume Intelligence – AI Resume Analyzer for Job Role

[![Streamlit App](https://img.shields.io/badge/🔴%20Live%20Demo-Click%20Here-brightgreen?style=for-the-badge&logo=streamlit)](https://resumeintelligence-by-saikumar.streamlit.app/)

---

## 🎯 Project Overview

Professional ATS Resume Analyzer built specifically for **Saikumar Yaramala** - B.Tech Electronics and Data Science student targeting fresher IT roles. This project demonstrates proficiency in Python, HTML, CSS, databases, and data science tools.

## 🚀 Features

- **Smart Resume Parsing**: Extract structured data from PDF, DOCX, and TXT files
- **ATS Compatibility Analysis**: Calculate ATS scores with detailed breakdowns
- **Skill Matching**: Advanced algorithm to match resume skills with job requirements
- **Visual Analytics**: Interactive charts and dashboards using Plotly
- **Job Recommendations**: Personalized job matching for Data Science and IT roles
- **Skill Gap Analysis**: Identify missing skills and learning paths
- **SQLite Database**: Persistent storage for all analysis data
- **Bootstrap-style UI**: Professional interface with custom CSS

## 🛠 Technologies Used

### Core Technologies

- **Python 3.11**: Main programming language
- **Streamlit**: Web application framework
- **SQLite**: Database for persistent storage
- **HTML/CSS**: Custom styling and Bootstrap-inspired design

### Python Libraries

- **Pandas & NumPy**: Data manipulation and analysis
- **NLTK**: Natural language processing
- **Scikit-learn**: Machine learning for text analysis
- **Plotly**: Interactive data visualization
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **WordCloud**: Skill visualization

## 📁 Project Structure

```
ats-resume-analyzer/
├── streamlit_app.py          # Main application file
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── resume_parser.py      # Resume text extraction and parsing
│   ├── database_manager.py   # SQLite database operations
│   ├── ats_analyzer.py       # ATS compatibility analysis
│   └── skill_matcher.py      # Skill matching algorithms
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md
└── ats_analyzer.db          # SQLite database (created automatically)
```

## 🔧 Installation & Setup

1. **Clone or download the project files**

2. **Install required packages**:

   ```bash
   pip install streamlit pandas numpy PyPDF2 python-docx nltk scikit-learn plotly wordcloud textstat spacy Pillow
   ```

3. **Download NLTK data** (automatic on first run):

   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

4. **Run the application**:

   ```bash
   streamlit run streamlit_app.py
   ```

5. **Access the app**: Open your browser to `http://localhost:8501`

## 💻 Usage Guide

### 1. Resume Analysis

- Upload your resume (PDF, DOCX, or TXT)
- System extracts personal info, skills, experience, education
- View structured data in organized sections

### 2. Job Matching

- Paste target job description
- Get ATS compatibility score
- See matched and missing skills
- Receive personalized recommendations

### 3. Analytics Dashboard

- View skill level analysis
- Track progress over time
- Analyze market trends for your skills

### 4. Career Recommendations

- Get job role suggestions based on current skills
- See learning paths for target roles
- Understand skill gaps and priorities

## 🎓 Educational Value

This project demonstrates:

### Data Science Skills

- **Data Processing**: Text extraction and cleaning
- **NLP Techniques**: Tokenization, TF-IDF, similarity analysis
- **Machine Learning**: Cosine similarity, feature extraction
- **Data Visualization**: Interactive charts and dashboards
- **Statistical Analysis**: Scoring algorithms and percentile calculations

### Software Engineering Skills

- **Object-Oriented Programming**: Modular class-based design
- **Database Design**: SQLite schema and operations
- **Web Development**: Streamlit framework with custom CSS
- **Error Handling**: Robust exception management
- **Code Organization**: Clean, maintainable code structure

### Professional Skills

- **Project Architecture**: Scalable, modular design
- **User Experience**: Intuitive interface design
- **Documentation**: Comprehensive README and code comments
- **Problem Solving**: Real-world application addressing ATS challenges

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)

1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Access via public URL

### Local Hosting

```bash
streamlit run streamlit_app.py --server.port 8501
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📊 Technical Highlights

### Resume Parsing Algorithm

- Multi-format support (PDF, DOCX, TXT)
- Intelligent text extraction with error handling
- Pattern recognition for contact information
- Section-based content organization

### ATS Scoring System

- Weighted scoring algorithm (35% keyword match, 25% skill match, etc.)
- TF-IDF similarity analysis
- Format compatibility checking
- Domain-specific keyword analysis

### Skill Matching Engine

- Comprehensive skill database for Data Science/IT
- Synonym recognition and normalization
- Career path recommendations
- Market trend analysis simulation

## 👨‍💼 Portfolio Highlights for Saikumar Yaramala

This project showcases expertise in:

- **Python Programming**: Advanced use of multiple libraries
- **Data Science Workflow**: End-to-end data processing pipeline
- **Database Management**: SQLite operations and schema design
- **Web Development**: Full-stack application with modern UI
- **Problem-Solving**: Addressing real industry challenge (ATS optimization)
- **Professional Development**: Tool useful for job search success

## 🔮 Future Enhancements

- **PDF Generation**: Create optimized resume PDFs
- **Email Integration**: Send analysis reports via email
- **Advanced ML Models**: Deep learning for better text analysis
- **API Integration**: Real job market data integration
- **Multi-language Support**: Support for different languages
- **Cloud Storage**: Integration with cloud storage services

## 📞 Contact

**Saikumar Yaramala**

- Field: B.Tech Electronics and Data Science
- Target: Fresher IT Roles in Data-Driven Positions
- Technologies: Python, Data Science, Machine Learning, Databases

---

_This project demonstrates comprehensive skills in Python development, data science, and web applications - perfect for showcasing technical abilities to potential employers in the IT and Data Science fields._
