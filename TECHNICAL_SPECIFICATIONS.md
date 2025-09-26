# AI MCQ Generator - Technical Specifications

## System Architecture Overview

### Technology Stack Selection

#### Backend Framework: FastAPI ✅
**Rationale**: FastAPI chosen for:
- **Async Support**: Native async/await for AI API calls and database operations
- **Auto Documentation**: Automatic OpenAPI/Swagger documentation generation
- **Type Safety**: Built-in request/response validation with Pydantic
- **Performance**: Superior performance for concurrent AI operations
- **Modern Python**: Full type hints integration and Python 3.9+ features
- **Ecosystem**: Excellent compatibility with PostgreSQL async drivers

#### Database: PostgreSQL ✅
**Rationale**: 
- **JSONB Support**: Native JSON storage for AI metadata and flexible content
- **Full-Text Search**: Built-in search capabilities for duplicate MCQ detection
- **ACID Compliance**: Reliable transactions for user data integrity
- **Async Support**: Compatible with FastAPI's async operations via asyncpg
- **Performance**: Advanced indexing (B-tree, GIN, GiST) for complex queries
- **Scalability**: Handles concurrent users and AI-generated content efficiently

#### AI Integration: Google Gemini API
**Configuration**:
```python
# Environment configuration
GEMINI_API_KEY = "your_api_key_here"
GEMINI_MODEL = "gemini-pro"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 2048
```

## **FastAPI + PostgreSQL Configuration**

#### Database Configuration
```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# PostgreSQL async connection configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://username:password@localhost:5432/aimcq_generator_db"
)

# Async engine optimized for AI workloads
async_engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # Handle concurrent AI requests
    max_overflow=0,         # Prevent connection exhaustion
    pool_pre_ping=True,     # Handle connection drops
    echo=False,             # Set to True for query debugging
    future=True             # Use SQLAlchemy 2.0 style
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency for FastAPI endpoints
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

#### FastAPI Application Setup
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    title="AI MCQ Generator API",
    description="Intelligent MCQ and flashcard generation system",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example endpoint using async PostgreSQL
@app.get("/api/v1/users/{user_id}/progress")
async def get_user_progress(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        # Async database operations here
        pass
```

## Detailed Component Specifications

### 1. PDF Processing Module

#### SmallDocling Integration
```python
class PDFProcessor:
    def __init__(self):
        self.docling = SmallDocling()
    
    async def extract_content(self, pdf_path: str) -> ExtractedContent:
        """Extract structured content from PDF"""
        # Implementation details for SmallDocling
        pass
    
    def validate_pdf(self, file_data: bytes) -> bool:
        """Validate PDF format and readability"""
        pass
    
    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract document metadata"""
        pass
```

#### Content Structure
```python
@dataclass
class ExtractedContent:
    raw_text: str
    structured_sections: List[Section]
    images: List[ImageData]
    tables: List[TableData]
    metadata: Dict[str, Any]
    confidence_score: float
```

### 2. AI Service Architecture

#### Gemini AI Service
```python
class GeminiAIService:
    def __init__(self, api_key: str):
        self.client = genai.GenerativeModel('gemini-pro')
        genai.configure(api_key=api_key)
    
    async def categorize_content(self, content: str) -> List[Topic]:
        """Categorize content into topics and subtopics"""
        prompt = self._build_categorization_prompt(content)
        response = await self.client.generate_content_async(prompt)
        return self._parse_topics(response.text)
    
    async def generate_mcqs(self, topic_content: str, difficulty: int, 
                           count: int, existing_questions: List[str]) -> List[MCQ]:
        """Generate MCQs avoiding duplicates"""
        prompt = self._build_mcq_prompt(topic_content, difficulty, count, existing_questions)
        response = await self.client.generate_content_async(prompt)
        return self._parse_mcqs(response.text)
    
    async def generate_flashcards(self, topic_content: str, count: int) -> List[Flashcard]:
        """Generate flashcards for topic"""
        prompt = self._build_flashcard_prompt(topic_content, count)
        response = await self.client.generate_content_async(prompt)
        return self._parse_flashcards(response.text)
    
    async def analyze_performance(self, user_responses: List[UserResponse]) -> PerformanceAnalysis:
        """Analyze user performance and provide insights"""
        prompt = self._build_analysis_prompt(user_responses)
        response = await self.client.generate_content_async(prompt)
        return self._parse_analysis(response.text)
```

#### AI Prompt Templates
```python
class PromptTemplates:
    CATEGORIZATION_PROMPT = """
    Analyze the following syllabus content and organize it into a hierarchical structure:
    
    Content: {content}
    
    Please organize this into topics and subtopics in JSON format:
    {{
        "topics": [
            {{
                "title": "Topic Title",
                "description": "Brief description",
                "subtopics": [
                    {{
                        "title": "Subtopic Title",
                        "description": "Brief description",
                        "content": "Relevant content"
                    }}
                ]
            }}
        ]
    }}
    """
    
    MCQ_GENERATION_PROMPT = """
    Generate {count} multiple-choice questions based on the following topic content.
    Difficulty Level: {difficulty}/5
    Topic Content: {content}
    
    Avoid generating questions similar to these existing ones:
    {existing_questions}
    
    Format each question as JSON:
    {{
        "question": "Question text",
        "options": {{
            "A": "Option A",
            "B": "Option B", 
            "C": "Option C",
            "D": "Option D"
        }},
        "correct_answer": "A",
        "explanation": "Explanation for the correct answer",
        "difficulty": {difficulty}
    }}
    """
```

### 3. Adaptive Learning Algorithm

#### Difficulty Progression System
```python
class DifficultyManager:
    def __init__(self):
        self.min_difficulty = 1
        self.max_difficulty = 5
        self.progression_threshold = 3  # Consecutive correct answers
        self.regression_threshold = 2   # Consecutive wrong answers
    
    def calculate_next_difficulty(self, user_progress: UserProgress, 
                                 recent_responses: List[UserResponse]) -> int:
        """Calculate next question difficulty based on performance"""
        current_difficulty = user_progress.current_difficulty_level
        consecutive_correct = user_progress.consecutive_correct
        
        # Analyze recent performance
        recent_correct = sum(1 for r in recent_responses[-5:] if r.is_correct)
        recent_accuracy = recent_correct / len(recent_responses[-5:]) if recent_responses else 0
        
        # Difficulty progression logic
        if consecutive_correct >= self.progression_threshold and recent_accuracy >= 0.8:
            return min(current_difficulty + 1, self.max_difficulty)
        elif consecutive_correct <= -self.regression_threshold and recent_accuracy <= 0.4:
            return max(current_difficulty - 1, self.min_difficulty)
        
        return current_difficulty
    
    def select_questions(self, topic_id: int, user_id: int, 
                        target_difficulty: int, count: int) -> List[MCQ]:
        """Select appropriate questions based on user history and difficulty"""
        # Get user's answered questions to avoid repetition
        answered_mcq_ids = self._get_answered_questions(user_id, topic_id)
        
        # Get available questions at target difficulty
        available_questions = self._get_available_questions(
            topic_id, target_difficulty, answered_mcq_ids
        )
        
        # If not enough questions at exact difficulty, include adjacent levels
        if len(available_questions) < count:
            adjacent_questions = self._get_adjacent_difficulty_questions(
                topic_id, target_difficulty, answered_mcq_ids, 
                needed_count=count - len(available_questions)
            )
            available_questions.extend(adjacent_questions)
        
        return random.sample(available_questions, min(count, len(available_questions)))
```

#### Performance Analytics Engine
```python
class PerformanceAnalyzer:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def analyze_user_performance(self, user_id: int, 
                               timeframe_days: int = 30) -> PerformanceReport:
        """Comprehensive performance analysis using async PostgreSQL"""
        # Async database queries for user responses
        responses_query = select(MCQUserResponse).where(
            MCQUserResponse.user_id == user_id,
            MCQUserResponse.answered_at >= datetime.now() - timedelta(days=timeframe_days)
        )
        result = await self.db.execute(responses_query)
        responses = result.scalars().all()
        
        overall_stats = await self._calculate_overall_stats(responses)
        topic_breakdown = await self._analyze_topic_performance(responses)
        difficulty_progression = await self._analyze_difficulty_progression(responses)
        learning_patterns = await self._identify_learning_patterns(responses)
        recommendations = await self._generate_recommendations(
            overall_stats, topic_breakdown, difficulty_progression
        )
        
        return PerformanceReport(
            overall_stats=overall_stats,
            topic_breakdown=topic_breakdown,
            difficulty_progression=difficulty_progression,
            learning_patterns=learning_patterns,
            recommendations=recommendations
        )
    
    async def identify_weak_areas(self, user_id: int) -> List[WeakArea]:
        """Identify topics/subtopics where user needs improvement using PostgreSQL"""
        # Async query for user progress with accuracy calculation
        progress_query = select(
            UserProgress,
            (UserProgress.correct_attempts / UserProgress.total_attempts).label('accuracy')
        ).where(
            UserProgress.user_id == user_id,
            UserProgress.total_attempts >= 5
        )
        
        result = await self.db.execute(progress_query)
        user_progress = result.all()
        
        weak_areas = []
        for progress, accuracy in user_progress:
            if accuracy < 0.6:
                weak_areas.append(WeakArea(
                    topic_id=progress.topic_id,
                    subtopic_id=progress.subtopic_id,
                    accuracy=accuracy,
                    attempts=progress.total_attempts,
                    severity=self._calculate_severity(accuracy, progress.total_attempts)
                ))
        
        return sorted(weak_areas, key=lambda x: x.severity, reverse=True)
```

### 4. Question Generation & Duplicate Prevention

#### Duplicate Detection System
```python
class DuplicateDetector:
    def __init__(self):
        self.similarity_threshold = 0.85
    
    def is_duplicate_question(self, new_question: str, 
                             existing_questions: List[str]) -> bool:
        """Check if question is too similar to existing ones"""
        for existing in existing_questions:
            similarity = self._calculate_similarity(new_question, existing)
            if similarity > self.similarity_threshold:
                return True
        return False
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two questions"""
        # Implementation using sentence transformers or simple token overlap
        # For MVP, can use simple token-based similarity
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0
    
    def generate_question_hash(self, question: str, options: List[str]) -> str:
        """Generate unique hash for question content"""
        content = f"{question}{''.join(sorted(options))}"
        return hashlib.sha256(content.encode()).hexdigest()
```

### 5. Spaced Repetition System

#### Flashcard Scheduling Algorithm
```python
class SpacedRepetitionScheduler:
    def __init__(self):
        self.initial_interval = 1  # days
        self.ease_factor = 2.5
        self.min_ease_factor = 1.3
        self.max_ease_factor = 2.5
    
    def calculate_next_review(self, flashcard_review: FlashcardReview) -> datetime:
        """Calculate next review date based on spaced repetition algorithm"""
        ease_rating = flashcard_review.ease_rating  # 1=Again, 2=Hard, 3=Good, 4=Easy
        current_interval = flashcard_review.interval_days or self.initial_interval
        
        if ease_rating == 1:  # Again - restart
            new_interval = 1
            new_ease_factor = max(
                flashcard_review.ease_factor - 0.2, 
                self.min_ease_factor
            )
        elif ease_rating == 2:  # Hard
            new_interval = max(1, int(current_interval * 0.6))
            new_ease_factor = max(
                flashcard_review.ease_factor - 0.15,
                self.min_ease_factor
            )
        elif ease_rating == 3:  # Good
            new_interval = int(current_interval * flashcard_review.ease_factor)
            new_ease_factor = flashcard_review.ease_factor
        else:  # Easy
            new_interval = int(current_interval * flashcard_review.ease_factor * 1.3)
            new_ease_factor = min(
                flashcard_review.ease_factor + 0.15,
                self.max_ease_factor
            )
        
        next_review = datetime.now() + timedelta(days=new_interval)
        return next_review, new_interval, new_ease_factor
```

### 6. API Rate Limiting & Caching

#### AI API Rate Management
```python
class AIRateLimiter:
    def __init__(self):
        self.request_cache = {}
        self.rate_limit_window = 60  # seconds
        self.max_requests_per_window = 60
    
    async def make_ai_request(self, prompt: str, cache_key: str = None) -> str:
        """Make AI request with rate limiting and caching"""
        # Check cache first
        if cache_key and cache_key in self.request_cache:
            cached_response, timestamp = self.request_cache[cache_key]
            if time.time() - timestamp < 3600:  # 1 hour cache
                return cached_response
        
        # Rate limiting logic
        await self._enforce_rate_limit()
        
        # Make actual AI request
        response = await self._make_request(prompt)
        
        # Cache response
        if cache_key:
            self.request_cache[cache_key] = (response, time.time())
        
        return response
```

### 7. Security Specifications

#### Authentication & Authorization
```python
class SecurityManager:
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET_KEY')
        self.jwt_algorithm = 'HS256'
        self.token_expiry = timedelta(hours=24)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id: int) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
```

### 8. Performance Optimization

#### Database Query Optimization
```python
from sqlalchemy import select, func, case, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

# Optimized async queries for common operations
class OptimizedQueries:
    @staticmethod
    async def get_user_progress_with_stats(db: AsyncSession, user_id: int):
        """Get user progress with aggregated statistics using async PostgreSQL"""
        query = select(
            UserProgress,
            func.count(MCQUserResponse.id).label('total_responses'),
            func.avg(case([(MCQUserResponse.is_correct == True, 1)], else_=0)).label('accuracy')
        ).outerjoin(
            MCQUserResponse, 
            and_(
                UserProgress.user_id == MCQUserResponse.user_id,
                or_(
                    UserProgress.topic_id == MCQ.topic_id,
                    UserProgress.subtopic_id == MCQ.subtopic_id
                )
            )
        ).where(UserProgress.user_id == user_id).group_by(UserProgress.id)
        
        result = await db.execute(query)
        return result.all()
    
    @staticmethod
    async def get_available_mcqs_optimized(db: AsyncSession, topic_id: int, user_id: int, difficulty: int):
        """Get available MCQs avoiding already answered ones using async PostgreSQL"""
        # Subquery for answered MCQs
        answered_subquery = select(MCQUserResponse.mcq_id).where(
            MCQUserResponse.user_id == user_id
        )
        
        # Main query for available MCQs
        mcqs_query = select(MCQ).where(
            MCQ.topic_id == topic_id,
            MCQ.difficulty_level == difficulty,
            MCQ.is_active == True,
            ~MCQ.id.in_(answered_subquery)
        )
        
        result = await db.execute(mcqs_query)
        return result.scalars().all()
    
    @staticmethod
    async def get_performance_analytics(db: AsyncSession, user_id: int, days: int = 30):
        """Get comprehensive performance analytics using PostgreSQL window functions"""
        query = select(
            MCQUserResponse.answered_at,
            MCQUserResponse.is_correct,
            MCQ.difficulty_level,
            func.lag(MCQUserResponse.is_correct).over(
                partition_by=MCQUserResponse.user_id,
                order_by=MCQUserResponse.answered_at
            ).label('previous_correct'),
            func.count().over(
                partition_by=[MCQUserResponse.user_id, MCQ.topic_id]
            ).label('topic_attempts'),
            func.avg(case([(MCQUserResponse.is_correct == True, 1.0)], else_=0.0)).over(
                partition_by=[MCQUserResponse.user_id, MCQ.topic_id]
            ).label('topic_accuracy')
        ).join(MCQ).where(
            MCQUserResponse.user_id == user_id,
            MCQUserResponse.answered_at >= datetime.now() - timedelta(days=days)
        ).order_by(MCQUserResponse.answered_at)
        
        result = await db.execute(query)
        return result.all()
    def get_user_progress_with_stats(user_id: int):
        """Get user progress with aggregated statistics"""
        return db.session.query(
            UserProgress,
            func.count(MCQUserResponse.id).label('total_responses'),
            func.avg(case([(MCQUserResponse.is_correct == True, 1)], else_=0)).label('accuracy')
        ).outerjoin(
            MCQUserResponse, 
            and_(
                UserProgress.user_id == MCQUserResponse.user_id,
                or_(
                    UserProgress.topic_id == MCQ.topic_id,
                    UserProgress.subtopic_id == MCQ.subtopic_id
                )
            )
        ).filter(UserProgress.user_id == user_id).group_by(UserProgress.id)
    
    @staticmethod
    def get_available_mcqs_optimized(topic_id: int, user_id: int, difficulty: int):
        """Get available MCQs avoiding already answered ones"""
        answered_subquery = db.session.query(MCQUserResponse.mcq_id).filter(
            MCQUserResponse.user_id == user_id
        ).subquery()
        
        return db.session.query(MCQ).filter(
            MCQ.topic_id == topic_id,
            MCQ.difficulty_level == difficulty,
            MCQ.is_active == True,
            ~MCQ.id.in_(answered_subquery)
        )
```

This technical specification provides the detailed implementation framework for building the AI MCQ Generator system with all the required features and performance considerations.