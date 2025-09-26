# AI MCQ Generator - Implementation Roadmap

## Quick Start Guide

### Prerequisites Checklist
- [ ] Python 3.9+ installed
- [ ] PostgreSQL installed and running
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Gemini API account and key

### Development Environment Setup

#### 1. Initial Project Setup Commands
```bash
# Install cookiecutter if not already installed
pip install cookiecutter

# Create project from template (we'll use a custom template)
cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage
# Or create basic structure manually

# Navigate to project directory
cd aimcq_generator

# Initialize git repository
git init
git add .
git commit -m "Initial project setup"
```

#### 2. Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

#### 3. Install Core Dependencies
```bash
# Install FastAPI with all extras (includes uvicorn, pydantic, etc.)
pip install "fastapi[all]>=0.104.1"

# Install PostgreSQL dependencies
pip install "sqlalchemy>=2.0.23"
pip install "alembic>=1.12.1" 
pip install "psycopg2-binary>=2.9.7"
pip install "asyncpg>=0.29.0"  # Async PostgreSQL driver

# Install core dependencies
pip install "python-dotenv>=1.0.0"
pip install "passlib[bcrypt]>=1.7.4"  # Password hashing
pip install "python-jose[cryptography]>=3.3.0"  # JWT handling
pip install "google-generativeai>=0.3.2"
pip install "python-multipart>=0.0.6"  # File uploads
pip install "aiofiles>=23.2.1"  # Async file operations

# Install development dependencies
pip install "pytest>=7.4.3"
pip install "pytest-asyncio>=0.21.1"  # For testing async functions
pip install "httpx>=0.25.0"  # For testing FastAPI endpoints
pip install "black>=23.10.1"
pip install "flake8>=6.1.0"
pip install "mypy>=1.7.1"
pip install "pre-commit>=3.5.0"

# PDF processing dependencies
pip install "PyPDF2>=3.0.1"
pip install "pdfplumber>=0.10.3"

# Save requirements
pip freeze > requirements.txt
```

## Phase-by-Phase Implementation

### Phase 1: Foundation Setup (Days 1-3)

#### Day 1: Project Structure Setup
```bash
# Create project structure
mkdir -p aimcq_generator/{backend,frontend,docs,scripts,tests}
mkdir -p aimcq_generator/backend/{app,migrations,tests,uploads}
mkdir -p aimcq_generator/backend/app/{models,services,api,core,utils}
mkdir -p aimcq_generator/backend/app/api/{v1,auth,endpoints}
```

**File Creation Priority:**
1. `.env.example` - Environment template
2. `backend/app/__init__.py` - App initialization
3. `backend/app/core/config.py` - Configuration management
4. `backend/app/core/database.py` - Database setup
5. `backend/requirements.txt` - Dependencies

#### Day 2: PostgreSQL Database Foundation
```bash
# Install and start PostgreSQL (macOS with Homebrew)
brew install postgresql@15
brew services start postgresql@15

# Create databases
createdb aimcq_generator_db
createdb aimcq_generator_test_db

# Set up Alembic for database migrations
cd backend
alembic init alembic

# Configure alembic.ini for PostgreSQL
# Edit alembic.ini: sqlalchemy.url = postgresql://localhost:5432/aimcq_generator_db
```

**Implementation Steps:**
1. Create SQLAlchemy models (users, documents, topics, mcqs)
2. Configure Alembic for migrations
3. Create initial migration
4. Test database connection

#### Day 3: Basic FastAPI Structure
**Create Basic FastAPI App:**
1. Main application setup (`backend/app/main.py`)
2. FastAPI router configuration with API versioning
3. PostgreSQL database connection setup
4. Basic health check and database connectivity endpoints
5. CORS middleware for React frontend
6. Automatic API documentation (OpenAPI/Swagger)

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="AI MCQ Generator API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
```

### Phase 2: Core Backend (Days 4-10)

#### Days 4-5: User Authentication System
**Implementation Order:**
1. User model and database operations
2. Password hashing utilities
3. JWT token management
4. Registration endpoint
5. Login endpoint
6. Protected route middleware

**Key Files to Create:**
- `backend/app/models/user.py`
- `backend/app/services/auth_service.py`
- `backend/app/api/v1/auth.py`
- `backend/app/core/security.py`

#### Days 6-7: Document Upload & Processing
**Implementation Steps:**
1. File upload handling
2. PDF validation
3. Basic text extraction (temporary solution)
4. Document storage system
5. Document management endpoints

**Key Files:**
- `backend/app/models/document.py`
- `backend/app/services/pdf_service.py`
- `backend/app/api/v1/documents.py`
- `backend/app/utils/file_handlers.py`

#### Days 8-10: Database Models & CRUD Operations
**Complete All Models:**
1. Topic and Subtopic models
2. MCQ and Flashcard models
3. User response tracking models
4. Service layer for each model
5. API endpoints for CRUD operations

### Phase 3: AI Integration (Days 11-17)

#### Days 11-12: Gemini AI Service Setup
```python
# Example implementation structure
# backend/app/services/ai_service.py

class GeminiAIService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def categorize_content(self, text: str) -> List[Dict]:
        # Implementation here
        pass
```

#### Days 13-14: Content Categorization
**Implementation Priority:**
1. Prompt engineering for topic extraction
2. Response parsing and validation
3. Topic hierarchy creation
4. Integration with database storage

#### Days 15-17: MCQ & Flashcard Generation
**Implementation Steps:**
1. MCQ generation prompts and parsing
2. Duplicate detection algorithm
3. Difficulty assignment logic
4. Flashcard generation system
5. Quality validation mechanisms

### Phase 4: Adaptive Learning (Days 18-24)

#### Days 18-20: Question Selection Algorithm
```python
# backend/app/services/adaptive_service.py

class AdaptiveLearningService:
    def select_next_questions(self, user_id: int, topic_id: int, 
                             session_length: int = 10) -> List[MCQ]:
        # Get user progress
        # Calculate appropriate difficulty
        # Select non-repeated questions
        # Return question set
        pass
```

#### Days 21-22: Performance Tracking
**Key Components:**
1. User session management
2. Response tracking system
3. Progress calculation algorithms
4. Performance analytics

#### Days 23-24: Recommendation Engine
**Implementation:**
1. Weakness identification algorithms
2. Study recommendation logic
3. Progress insights generation
4. Personalized learning paths

### Phase 5: Frontend Development (Days 25-35)

#### Days 25-27: Frontend Setup & Authentication
```bash
# Frontend setup (React with TypeScript)
npx create-react-app frontend --template typescript
cd frontend
npm install axios react-router-dom @mui/material
```

**Core Components to Build:**
1. Authentication forms (Login/Register)
2. Protected route wrapper
3. API client setup
4. Basic layout and navigation

#### Days 28-30: Document Management UI
**Components:**
1. File upload interface
2. Document list view
3. Processing status indicators
4. Topic/subtopic browser

#### Days 31-33: MCQ Interface
**Features:**
1. Question display component
2. Answer selection interface
3. Real-time feedback
4. Session progress tracking
5. Results summary

#### Days 34-35: Analytics Dashboard
**Components:**
1. Performance charts
2. Progress visualization
3. Weakness identification display
4. Recommendation interface

### Phase 6: Testing & Optimization (Days 36-42)

#### Days 36-38: Backend Testing
```python
# Example test structure
# backend/tests/test_auth.py

class TestAuthentication:
    def test_user_registration(self):
        # Test user registration endpoint
        pass
    
    def test_login_success(self):
        # Test successful login
        pass
    
    def test_protected_routes(self):
        # Test JWT authentication
        pass
```

#### Days 39-40: Integration Testing
**Test Scenarios:**
1. End-to-end PDF processing workflow
2. AI generation quality validation
3. Adaptive learning algorithm testing
4. Performance under load

#### Days 41-42: Performance Optimization
**Optimization Areas:**
1. Database query optimization
2. API response caching
3. AI request batching
4. Frontend performance tuning

## Environment Configuration

### Required Environment Variables
```bash
# .env file template
# PostgreSQL Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/aimcq_generator_db
DATABASE_TEST_URL=postgresql+asyncpg://username:password@localhost:5432/aimcq_generator_test_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048

# File Upload Configuration
MAX_UPLOAD_SIZE_MB=50
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=pdf

# FastAPI Application Configuration
DEBUG=True
ENVIRONMENT=development
API_V1_STR=/api/v1
PROJECT_NAME="AI MCQ Generator"
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Deployment Preparation

### Docker Configuration
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: aimcq_generator_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:password@postgres:5432/aimcq_generator_db
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      REACT_APP_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

## Success Milestones

### Week 1 Milestones
- [ ] Project structure created
- [ ] Database schema implemented
- [ ] Basic API endpoints working
- [ ] Authentication system functional

### Week 2 Milestones
- [ ] PDF upload and basic processing working
- [ ] AI integration completed
- [ ] Content categorization functional
- [ ] MCQ generation working

### Week 3 Milestones
- [ ] Adaptive learning algorithm implemented
- [ ] Frontend basic structure completed
- [ ] User authentication UI working
- [ ] Document management interface functional

### Week 4 Milestones
- [ ] Complete MCQ interface working
- [ ] Performance analytics implemented
- [ ] Testing suite completed
- [ ] Ready for deployment

## Risk Mitigation Strategies

### Technical Risks
1. **AI API Rate Limits**: Implement request caching and batching
2. **Performance Issues**: Use database indexing and query optimization
3. **Data Quality**: Implement validation and manual review processes
4. **Security Vulnerabilities**: Follow security best practices and conduct audits

### Development Risks
1. **Scope Creep**: Stick to MVP requirements initially
2. **Timeline Delays**: Build iteratively with working prototypes
3. **Integration Issues**: Test integrations early and frequently
4. **Quality Issues**: Implement comprehensive testing from day one

This roadmap provides a structured approach to building the AI MCQ Generator with clear milestones and practical implementation steps.