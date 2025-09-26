# AI MCQ Generator - Development Plan

## Project Development Phases

### Phase 1: Project Setup & Foundation (Week 1-2)

#### 1.1 Project Initialization
- [ ] Set up Cookiecutter Python project template
- [ ] Configure virtual environment and dependencies
- [ ] Set up project structure and basic configuration
- [ ] Initialize Git repository and basic documentation

#### 1.2 Core Dependencies Setup
```python
# Key dependencies to include
dependencies = [
    "fastapi[all]>=0.104.1",  # FastAPI with all extras (uvicorn, etc.)
    "sqlalchemy>=2.0.23",  # ORM with async support
    "alembic>=1.12.1",  # Database migrations
    "psycopg2-binary>=2.9.7",  # PostgreSQL adapter
    "asyncpg>=0.29.0",  # Async PostgreSQL driver
    "python-dotenv>=1.0.0",  # Environment variables
    "passlib[bcrypt]>=1.7.4",  # Password hashing
    "python-jose[cryptography]>=3.3.0",  # JWT tokens
    "google-generativeai>=0.3.2",  # Gemini AI
    "pydantic>=2.4.2",  # Data validation (FastAPI compatible)
    "python-multipart>=0.0.6",  # File upload support
    "pytest>=7.4.3",  # Testing
    "pytest-asyncio>=0.21.1",  # Async testing
    "black>=23.10.1",  # Code formatting
    "flake8>=6.1.0",  # Linting
]
```

#### 1.3 Database Setup
- [ ] Set up PostgreSQL database (local development)
- [ ] Create database schema using SQLAlchemy models
- [ ] Set up Alembic for database migrations
- [ ] Create seed data for testing

#### 1.4 Configuration Management
- [ ] Environment-based configuration system
- [ ] Secure API key management
- [ ] Database connection configuration
- [ ] Logging setup

### Phase 2: Core Backend Development (Week 3-5)

#### 2.1 User Authentication & Management
- [ ] User registration and login system
- [ ] JWT-based authentication
- [ ] User profile management
- [ ] Password reset functionality

#### 2.2 PDF Processing Module
- [ ] SmallDocling integration for PDF extraction
- [ ] File upload handling and validation
- [ ] Document storage and metadata management
- [ ] Error handling for corrupted/unsupported files

#### 2.3 Database Models Implementation
- [ ] SQLAlchemy models for all entities
- [ ] Relationship definitions and constraints
- [ ] Database migration scripts
- [ ] CRUD operations and repositories

#### 2.4 Basic FastAPI Endpoints
```python
# Core FastAPI API structure
from fastapi import FastAPI, APIRouter

app = FastAPI(
    title="AI MCQ Generator API",
    description="Intelligent MCQ and flashcard generation system",
    version="1.0.0"
)

# API endpoint structure
api_endpoints = {
    "authentication": [
        "POST /api/v1/auth/register",
        "POST /api/v1/auth/login", 
        "POST /api/v1/auth/refresh",
        "POST /api/v1/auth/logout"
    ],
    "documents": [
        "POST /api/v1/documents/upload",
        "GET /api/v1/documents",
        "GET /api/v1/documents/{id}",
        "DELETE /api/v1/documents/{id}"
    ],
    "topics": [
        "GET /api/v1/topics/document/{doc_id}",
        "GET /api/v1/topics/{id}",
        "GET /api/v1/subtopics/topic/{topic_id}"
    ],
    "mcqs": [
        "POST /api/v1/mcqs/generate",
        "GET /api/v1/mcqs/session/{session_id}",
        "POST /api/v1/mcqs/answer"
    ]
}
```

### Phase 3: AI Integration (Week 6-8)

#### 3.1 Gemini AI Integration
- [ ] API client setup and configuration
- [ ] Content categorization service
- [ ] MCQ generation service
- [ ] Flashcard generation service
- [ ] Error handling and retry logic

#### 3.2 Content Categorization System
- [ ] AI-powered topic extraction from PDFs
- [ ] Hierarchical content organization
- [ ] Confidence scoring for categorizations
- [ ] Manual review and editing capabilities

#### 3.3 MCQ Generation Engine
- [ ] Context-aware question generation
- [ ] Difficulty level assignment
- [ ] Duplicate detection and prevention
- [ ] Quality validation and filtering

#### 3.4 AI Service Architecture
```python
# AI service structure
class AIService:
    def extract_topics(self, content: str) -> List[Topic]
    def generate_mcqs(self, topic: Topic, difficulty: int, count: int) -> List[MCQ]
    def generate_flashcards(self, topic: Topic, count: int) -> List[Flashcard]
    def analyze_performance(self, user_responses: List[Response]) -> AnalysisReport
```

### Phase 4: Adaptive Learning System (Week 9-11)

#### 4.1 MCQ Session Management
- [ ] Session creation and management
- [ ] Question selection algorithm
- [ ] Real-time difficulty adjustment
- [ ] Response tracking and validation

#### 4.2 Difficulty Progression Algorithm
```python
class DifficultyManager:
    def calculate_next_difficulty(self, user_progress: UserProgress, 
                                 recent_responses: List[Response]) -> int
    def select_questions(self, topic_id: int, user_id: int, 
                        difficulty: int, count: int) -> List[MCQ]
    def update_user_progress(self, user_id: int, responses: List[Response])
```

#### 4.3 Performance Analytics
- [ ] User performance tracking
- [ ] Weakness identification system
- [ ] Progress visualization data
- [ ] Recommendation engine

#### 4.4 Spaced Repetition System
- [ ] Flashcard review scheduling
- [ ] Memory retention algorithm
- [ ] Review session management
- [ ] Progress tracking for flashcards

### Phase 5: Frontend Development (Week 12-15)

#### 5.1 Web Interface Setup
- [ ] Choose frontend framework (React/Vue.js recommended)
- [ ] Set up build system and development environment
- [ ] Design responsive UI/UX
- [ ] Authentication integration

#### 5.2 Core User Interfaces
```
Key UI Components:
├── Authentication (Login/Register)
├── Dashboard (Overview & Statistics)
├── Document Management (Upload & View)
├── Topic Browser (Hierarchical View)
├── MCQ Interface (Question & Answer)
├── Flashcard Interface (Study Mode)
├── Progress Analytics (Charts & Reports)
└── Settings (Profile & Configuration)
```

#### 5.3 Interactive Features
- [ ] Real-time MCQ sessions
- [ ] Progress visualization
- [ ] Topic/subtopic navigation
- [ ] Performance analytics dashboard

### Phase 6: Testing & Quality Assurance (Week 16-17)

#### 6.1 Unit Testing
- [ ] Model and service layer tests
- [ ] API endpoint testing
- [ ] AI integration testing
- [ ] Database operation testing

#### 6.2 Integration Testing
- [ ] End-to-end workflow testing
- [ ] PDF processing pipeline tests
- [ ] AI generation quality tests
- [ ] Performance and load testing

#### 6.3 User Acceptance Testing
- [ ] Manual testing scenarios
- [ ] Edge case validation
- [ ] Error handling verification
- [ ] Security testing

### Phase 7: Deployment & Documentation (Week 18)

#### 7.1 Deployment Setup
- [ ] Production environment configuration
- [ ] Database migration to production
- [ ] Environment variable management
- [ ] CI/CD pipeline setup

#### 7.2 Documentation
- [ ] API documentation (OpenAPI/Swagger)
- [ ] User manual and tutorials
- [ ] Developer documentation
- [ ] Deployment and maintenance guides

## Technical Architecture

### 1. Project Structure (FastAPI + PostgreSQL)
```
aimcq_generator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app initialization
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── topic.py
│   │   │   └── mcq.py
│   │   ├── api/                 # FastAPI routers
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── documents.py
│   │   │   │   ├── topics.py
│   │   │   │   └── mcqs.py
│   │   │   └── deps.py          # Dependencies
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── ai_service.py
│   │   │   └── mcq_service.py
│   │   ├── core/                # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── mcq.py
│   │   └── utils/
│   ├── alembic/                 # Database migrations
│   ├── tests/
│   └── requirements.txt
├── frontend/                    # React TypeScript
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
├── scripts/
└── docker-compose.yml           # PostgreSQL + FastAPI + React
```

### 2. Key Services Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   AI Services   │
│   (React+TS)    │◄──►│   Backend       │◄──►│   (Gemini)      │
│   Port: 3000    │    │   Port: 8000    │    │   API           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   Database      │
                       │   Port: 5432    │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  File Storage   │
                       │  (Local/S3)     │
                       └─────────────────┘
```

### 3. Development Best Practices
- [ ] Follow PEP 8 coding standards
- [ ] Implement comprehensive error handling
- [ ] Use dependency injection for services
- [ ] Implement proper logging and monitoring
- [ ] Follow RESTful API design principles
- [ ] Implement proper security measures
- [ ] Use database transactions appropriately
- [ ] Implement caching where beneficial

### 4. Risk Mitigation
- **API Rate Limits**: Implement caching and request batching
- **Data Privacy**: Encrypt sensitive user data
- **Scalability**: Design for horizontal scaling
- **AI Quality**: Implement content validation and human review
- **Performance**: Optimize database queries and implement caching

## Success Criteria

### Functional Requirements Met
- [ ] Users can upload and process PDF syllabi
- [ ] AI categorizes content into topics/subtopics
- [ ] System generates non-repetitive MCQs
- [ ] Difficulty increases based on performance
- [ ] Performance analytics and recommendations work
- [ ] Flashcard system with spaced repetition

### Performance Requirements Met
- [ ] PDF processing completes within 2 minutes
- [ ] MCQ generation completes within 30 seconds
- [ ] System supports 100+ concurrent users
- [ ] Database queries respond within 500ms
- [ ] 99.9% uptime availability

### Quality Requirements Met
- [ ] 90%+ test coverage
- [ ] No critical security vulnerabilities
- [ ] Responsive UI on all device sizes
- [ ] Comprehensive error handling
- [ ] Complete documentation