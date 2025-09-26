# AI MCQ Generator Project Requirements

## Project Overview
An intelligent MCQ and flashcard generation system that extracts information from syllabus PDFs, categorizes content using AI, and generates adaptive assessments with difficulty progression.

## Core Requirements

### 1. Technology Stack
- **Framework**: Python with Cookiecutter project template
- **Backend**: FastAPI (chosen for async support and automatic API documentation)
- **Database**: PostgreSQL (chosen for JSONB support, full-text search, and scalability)
- **PDF Processing**: SmallDocling for PDF information extraction
- **AI Integration**: Gemini Free API (with configurable API key)
- **Frontend**: React with TypeScript (Web interface)

### 2. Core Features

#### 2.1 PDF Processing & Information Extraction
- Users can upload syllabus PDF files
- SmallDocling extracts structured information from PDFs
- Extracted content is stored in the database linked to user profiles

#### 2.2 User Management System
- User registration and authentication
- Individual user profiles and databases
- Personal learning progress tracking
- User-specific content storage

#### 2.3 AI-Powered Content Categorization
- Gemini API categorizes extracted content into topics and subtopics
- Hierarchical topic structure (Topic → Subtopic → Content)
- Intelligent content organization and tagging

#### 2.4 Adaptive MCQ Generation System
- **Non-Repetitive MCQs**: Track generated questions to avoid duplicates
- **Difficulty Progression**: Questions get harder as user answers correctly
- **Topic-Specific Generation**: MCQs generated for specific topics/subtopics
- **Performance Tracking**: Store user responses and accuracy rates

#### 2.5 Flashcard System
- AI-generated flashcards for topics and subtopics
- Spaced repetition algorithm integration
- Progress tracking for flashcard reviews

#### 2.6 Performance Analytics & Recommendations
- Analyze user MCQ performance data
- Identify knowledge gaps and weak areas
- AI-powered recommendations for focus areas
- Progress visualization and insights

### 3. Database Requirements

#### 3.1 Core Entities
- **Users**: Authentication and profile information
- **Documents**: Uploaded PDFs and metadata
- **Topics/Subtopics**: Hierarchical content organization
- **MCQs**: Generated questions with difficulty levels
- **Flashcards**: Generated review cards
- **User Responses**: Performance tracking and analytics
- **Learning Sessions**: User study sessions and progress

#### 3.2 Key Relationships
- Users → Documents (1:N)
- Documents → Topics (1:N)
- Topics → Subtopics (1:N)
- Topics/Subtopics → MCQs (1:N)
- Topics/Subtopics → Flashcards (1:N)
- Users → User Responses (1:N)
- MCQs → User Responses (1:N)

### 4. Configuration Requirements
- Configurable Gemini API key storage
- Environment-based configuration management
- PostgreSQL database connection configuration
- FastAPI server configuration (CORS, middleware)
- PDF processing settings
- JWT authentication configuration

### 5. Performance Requirements
- No duplicate MCQ generation for same user/topic combination
- Adaptive difficulty algorithm based on user performance
- Efficient PDF processing and content extraction
- Real-time AI response integration

### 6. Future Extensibility
- Support for multiple AI providers (not just Gemini)
- Multiple file format support beyond PDFs
- Integration with learning management systems
- Mobile application support
- Advanced analytics and reporting