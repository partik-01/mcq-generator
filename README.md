# AI MCQ Generator 🎓🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)

> **🚀 Current Status: Phase 2 Complete - Core Backend Development**
> 
> ✅ Authentication System | ✅ Database Schema | ✅ API Endpoints | ✅ JWT Security

## 📋 Project Summary

**AI MCQ Generator** is an intelligent learning platform that transforms educational content from PDF syllabi into personalized, adaptive assessments. The system leverages AI to extract, categorize, and generate contextual multiple-choice questions and flashcards with difficulty progression based on user performance.

## 🎯 Key Features

### Core Functionality
- **PDF Processing**: Upload syllabus PDFs with SmallDocling extraction
- **AI Categorization**: Automatic content organization into topics/subtopics using Gemini AI
- **Adaptive MCQs**: Non-repetitive questions with increasing difficulty based on performance
- **Smart Flashcards**: AI-generated review cards with spaced repetition
- **Performance Analytics**: Detailed insights into learning progress and weak areas
- **Personalized Recommendations**: AI-driven study suggestions based on user data

### Technical Highlights
- **Technology Stack**: Python, FastAPI, PostgreSQL, React/TypeScript
- **AI Integration**: Google Gemini API for content generation and analysis
- **Adaptive Algorithm**: Dynamic difficulty adjustment based on user responses
- **Scalable Architecture**: Microservices-ready design with comprehensive testing

## 📁 Project Structure

```
aimcq_generator/
├── 📄 PROJECT_REQUIREMENTS.md      # Detailed feature requirements
├── 📄 DATABASE_SCHEMA.md           # Complete database design
├── 📄 DEVELOPMENT_PLAN.md          # Phase-by-phase development strategy
├── 📄 TECHNICAL_SPECIFICATIONS.md  # Detailed technical implementation
├── 📄 IMPLEMENTATION_ROADMAP.md    # Step-by-step implementation guide
├── 📄 README.md                    # This overview document
├── 🔧 backend/                     # Python FastAPI backend (to be created)
├── 🎨 frontend/                    # React TypeScript frontend (to be created)
├── 📚 docs/                        # Additional documentation
└── 🐳 docker-compose.yml          # Container orchestration (to be created)
```

## 📖 Documentation Guide

### 1. **PROJECT_REQUIREMENTS.md**
   - Complete feature specifications
   - User stories and acceptance criteria
   - Technology stack justification
   - Performance and scalability requirements

### 2. **DATABASE_SCHEMA.md**
   - Comprehensive entity relationship design
   - SQL table definitions with constraints
   - Indexing strategies for performance
   - Data integrity and relationship management

### 3. **DEVELOPMENT_PLAN.md**
   - 6-phase development approach (18 weeks)
   - Resource allocation and timeline
   - Risk assessment and mitigation strategies
   - Quality assurance and testing protocols

### 4. **TECHNICAL_SPECIFICATIONS.md**
   - Detailed component architecture
   - AI integration patterns and algorithms
   - Security implementation details
   - Performance optimization strategies

### 5. **IMPLEMENTATION_ROADMAP.md**
   - Day-by-day implementation schedule
   - Code structure and file organization
   - Environment setup and configuration
   - Deployment preparation guidelines

## 🚀 Getting Started

### Phase 1: Review & Planning (Recommended)
1. **Read PROJECT_REQUIREMENTS.md** - Understand the complete feature set
2. **Study DATABASE_SCHEMA.md** - Familiarize yourself with data relationships
3. **Review DEVELOPMENT_PLAN.md** - Understand the development phases
4. **Check TECHNICAL_SPECIFICATIONS.md** - Review implementation details

### Phase 2: Environment Setup
1. Follow the environment setup in **IMPLEMENTATION_ROADMAP.md**
2. Set up development tools and dependencies
3. Configure database and AI API access
4. Initialize project structure using Cookiecutter template

### Phase 3: Incremental Development
Follow the phase-by-phase approach outlined in the development plan:
- **Weeks 1-2**: Project foundation and basic backend
- **Weeks 3-5**: Core backend development with database
- **Weeks 6-8**: AI integration and content processing
- **Weeks 9-11**: Adaptive learning algorithms
- **Weeks 12-15**: Frontend development
- **Weeks 16-18**: Testing, optimization, and deployment

## 🎯 Current Status & Quick Start

### ✅ What's Implemented (Phase 2 Complete)

**🗄️ Database Infrastructure:**
- Complete PostgreSQL schema with 10 tables
- User authentication and session management
- MCQ, Topics, Documents, and Learning analytics models
- Database migrations with Alembic

**🔐 Authentication System:**
- JWT-based user authentication
- Password hashing with bcrypt
- Protected API endpoints
- User registration and login

**🌐 API Endpoints:**
- FastAPI application with auto-documentation
- Authentication endpoints (`/register`, `/login`, `/me`)
- CORS configuration for frontend
- Comprehensive error handling

### 🚀 Quick Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/partik-01/mcq-generator.git
cd mcq-generator

# 2. Set up Python environment
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Set up PostgreSQL (macOS with Homebrew)
brew install postgresql@15
brew services start postgresql@15
createdb aimcq_generator_db

# 5. Configure environment
cp ../.env.example ../.env
# Edit .env with your database URL and Gemini API key

# 6. Run database migrations
alembic upgrade head

# 7. Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 📚 API Documentation
Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### 🧪 Test the Authentication
```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123", "first_name": "Test", "last_name": "User"}'

# Login and get JWT token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}'
```

## 🔧 Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+) with async support
- **Database**: PostgreSQL with SQLAlchemy 2.0+ (async ORM)
- **AI Integration**: Google Gemini API with rate limiting
- **Authentication**: JWT with PassLib bcrypt password hashing
- **PDF Processing**: SmallDocling + PyPDF2 fallback
- **API Documentation**: Automatic OpenAPI/Swagger generation

### Frontend
- **Framework**: React with TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: React Context + useReducer
- **API Client**: Axios with request/response interceptors

### DevOps & Tools
- **Containerization**: Docker & Docker Compose (PostgreSQL + FastAPI + React)
- **Database Migrations**: Alembic with async PostgreSQL support
- **Testing**: Pytest with pytest-asyncio (backend) + Jest (frontend)
- **Code Quality**: Black, Flake8, MyPy, ESLint, Prettier
- **Development**: FastAPI auto-reload with PostgreSQL connection pooling

## 🗺️ Development Roadmap

### 🚧 Phase 3: AI Integration & PDF Processing (Next)
- **PDF Upload & Processing**: Document upload endpoints with SmallDocling
- **Gemini AI Services**: Content categorization and topic extraction  
- **Document Management**: File storage, processing status, metadata
- **Content Pipeline**: PDF → Text → AI Analysis → Topics/Subtopics

### 🎯 Phase 4: MCQ Generation & Learning Engine
- **AI-Powered MCQ Creation**: Generate questions from extracted content
- **Adaptive Difficulty**: Dynamic question selection based on performance
- **Learning Sessions**: Manage user practice sessions with progress tracking
- **Performance Analytics**: Track accuracy, time, difficulty progression

### 🎨 Phase 5: Frontend Development
- **React Dashboard**: User interface for document management
- **Learning Interface**: Interactive MCQ practice sessions
- **Progress Visualizations**: Charts and analytics for performance tracking
- **Responsive Design**: Mobile and desktop optimization

### 🚀 Phase 6: Advanced Features & Deployment
- **Spaced Repetition**: Flashcard system with optimal review scheduling
- **Multi-format Support**: Additional document types beyond PDF
- **Advanced Analytics**: ML-driven insights and recommendations
- **Production Deployment**: Docker, CI/CD, cloud hosting

## 🎯 Success Criteria

### Functional Goals
- ✅ PDF upload and content extraction working
- ✅ AI-powered topic categorization functional
- ✅ Non-repetitive MCQ generation with difficulty progression
- ✅ Performance tracking and analytics dashboard
- ✅ User authentication and profile management
- ✅ Responsive web interface

### Technical Goals
- ✅ 90%+ test coverage
- ✅ Sub-500ms API response times
- ✅ Support for 100+ concurrent users
- ✅ Secure authentication and data protection
- ✅ Scalable and maintainable architecture

### Business Goals
- ✅ Personalized learning experience
- ✅ Measurable improvement in user knowledge retention
- ✅ Intuitive and engaging user interface
- ✅ Comprehensive performance analytics

## 🛣️ Development Approach

### Iterative Development Strategy
1. **MVP First**: Focus on core functionality before advanced features
2. **Test-Driven Development**: Write tests alongside implementation
3. **Continuous Integration**: Automated testing and code quality checks
4. **User Feedback Loops**: Regular testing with target users
5. **Performance Monitoring**: Continuous optimization and monitoring

### Quality Assurance
- **Code Reviews**: Peer review for all major changes
- **Automated Testing**: Unit, integration, and end-to-end tests
- **Security Audits**: Regular security vulnerability assessments
- **Performance Testing**: Load testing and optimization
- **User Acceptance Testing**: Real-world usage validation

## 🤝 Next Steps

1. **Review all documentation** to understand the complete scope
2. **Set up development environment** following the roadmap
3. **Start with Phase 1** of the development plan
4. **Follow the implementation roadmap** for daily tasks
5. **Regular progress reviews** against milestones

## 📞 Support & Resources

### Documentation References
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Google Gemini AI**: https://ai.google.dev/docs
- **React TypeScript**: https://react-typescript-cheatsheet.netlify.app/
- **PostgreSQL**: https://www.postgresql.org/docs/

### Development Tools
- **VS Code Extensions**: Python, TypeScript, SQLTools
- **Database Tools**: pgAdmin, DBeaver
- **API Testing**: Postman, Insomnia
- **Version Control**: Git with conventional commits

---

**Note**: This project is designed to be built incrementally. Start with the foundation and gradually add features according to the development plan. Each phase builds upon the previous one, ensuring a solid, scalable system.

Ready to start building? Begin with the **IMPLEMENTATION_ROADMAP.md** for step-by-step instructions! 🚀