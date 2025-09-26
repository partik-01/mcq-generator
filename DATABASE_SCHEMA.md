# Database Schema Design

## Overview
This document outlines the database schema for the AI MCQ Generator project, designed to support user management, content organization, adaptive learning, and performance analytics.

## Entity Relationship Diagram (Conceptual)

```
Users (1) ←→ (N) Documents ←→ (N) Topics ←→ (N) Subtopics
  ↓                                ↓              ↓
UserSessions (N)              MCQs (N)     Flashcards (N)
  ↓                              ↓              ↓
UserResponses (N) ←→ MCQs    UserResponses   FlashcardReviews
```

## Detailed Schema

### 1. Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP
);
```

### 2. Documents Table
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(50),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    extraction_completed_at TIMESTAMP,
    document_hash VARCHAR(64) UNIQUE, -- To prevent duplicate uploads
    metadata JSONB -- Store additional document metadata
);
```

### 3. Topics Table
```sql
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    extracted_content TEXT,
    topic_order INTEGER, -- Order within the document
    ai_confidence_score DECIMAL(3,2), -- AI confidence in categorization (0.00-1.00)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Subtopics Table
```sql
CREATE TABLE subtopics (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    extracted_content TEXT,
    subtopic_order INTEGER, -- Order within the topic
    ai_confidence_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. MCQs Table
```sql
CREATE TABLE mcqs (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    subtopic_id INTEGER REFERENCES subtopics(id),
    question TEXT NOT NULL,
    option_a VARCHAR(500) NOT NULL,
    option_b VARCHAR(500) NOT NULL,
    option_c VARCHAR(500) NOT NULL,
    option_d VARCHAR(500) NOT NULL,
    correct_answer CHAR(1) NOT NULL CHECK (correct_answer IN ('A', 'B', 'C', 'D')),
    difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
    explanation TEXT,
    question_hash VARCHAR(64) UNIQUE, -- To prevent duplicate questions
    ai_generated_metadata JSONB, -- Store AI generation parameters
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Ensure either topic_id or subtopic_id is provided, but not both
    CONSTRAINT check_topic_or_subtopic CHECK (
        (topic_id IS NOT NULL AND subtopic_id IS NULL) OR 
        (topic_id IS NULL AND subtopic_id IS NOT NULL)
    )
);
```

### 6. Flashcards Table
```sql
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    subtopic_id INTEGER REFERENCES subtopics(id),
    front_text TEXT NOT NULL,
    back_text TEXT NOT NULL,
    difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
    card_type VARCHAR(20) DEFAULT 'basic', -- basic, cloze, image, etc.
    ai_generated_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Ensure either topic_id or subtopic_id is provided, but not both
    CONSTRAINT check_flashcard_topic_or_subtopic CHECK (
        (topic_id IS NOT NULL AND subtopic_id IS NULL) OR 
        (topic_id IS NULL AND subtopic_id IS NOT NULL)
    )
);
```

### 7. User Learning Sessions Table
```sql
CREATE TABLE user_learning_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_type VARCHAR(20) NOT NULL, -- 'mcq', 'flashcard', 'mixed'
    topic_id INTEGER REFERENCES topics(id),
    subtopic_id INTEGER REFERENCES subtopics(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    session_score DECIMAL(5,2), -- Percentage score
    time_spent_seconds INTEGER,
    is_completed BOOLEAN DEFAULT FALSE
);
```

### 8. MCQ User Responses Table
```sql
CREATE TABLE mcq_user_responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    mcq_id INTEGER REFERENCES mcqs(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES user_learning_sessions(id) ON DELETE CASCADE,
    selected_answer CHAR(1) CHECK (selected_answer IN ('A', 'B', 'C', 'D')),
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER,
    difficulty_at_time INTEGER, -- MCQ difficulty when answered
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate responses for same MCQ in same session
    UNIQUE(session_id, mcq_id)
);
```

### 9. Flashcard Reviews Table
```sql
CREATE TABLE flashcard_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    flashcard_id INTEGER REFERENCES flashcards(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES user_learning_sessions(id) ON DELETE CASCADE,
    ease_rating INTEGER CHECK (ease_rating BETWEEN 1 AND 4), -- 1=Again, 2=Hard, 3=Good, 4=Easy
    time_taken_seconds INTEGER,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_review_date TIMESTAMP -- Spaced repetition scheduling
);
```

### 10. User Progress Tracking Table
```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id),
    subtopic_id INTEGER REFERENCES subtopics(id),
    mastery_level DECIMAL(3,2) DEFAULT 0.00, -- 0.00-1.00 mastery percentage
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    current_difficulty_level INTEGER DEFAULT 1,
    last_activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consecutive_correct INTEGER DEFAULT 0,
    needs_review BOOLEAN DEFAULT FALSE,
    
    -- Ensure either topic_id or subtopic_id is provided, but not both
    CONSTRAINT check_progress_topic_or_subtopic CHECK (
        (topic_id IS NOT NULL AND subtopic_id IS NULL) OR 
        (topic_id IS NULL AND subtopic_id IS NOT NULL)
    ),
    
    -- Unique constraint for user-topic/subtopic combination
    UNIQUE(user_id, topic_id, subtopic_id)
);
```

### 11. AI Configuration Table
```sql
CREATE TABLE ai_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(50) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    is_sensitive BOOLEAN DEFAULT FALSE, -- For API keys, passwords, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default configurations
INSERT INTO ai_config (config_key, config_value, description, is_sensitive) VALUES
('gemini_api_key', '', 'Gemini AI API Key', TRUE),
('gemini_model', 'gemini-pro', 'Gemini model to use', FALSE),
('max_mcqs_per_topic', '50', 'Maximum MCQs to generate per topic', FALSE),
('difficulty_increase_threshold', '3', 'Consecutive correct answers to increase difficulty', FALSE);
```

## Indexes for Performance

```sql
-- User-related indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Document-related indexes
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_processing_status ON documents(processing_status);

-- Topic and subtopic indexes
CREATE INDEX idx_topics_document_id ON topics(document_id);
CREATE INDEX idx_subtopics_topic_id ON subtopics(topic_id);

-- MCQ and flashcard indexes
CREATE INDEX idx_mcqs_topic_id ON mcqs(topic_id);
CREATE INDEX idx_mcqs_subtopic_id ON mcqs(subtopic_id);
CREATE INDEX idx_mcqs_difficulty ON mcqs(difficulty_level);
CREATE INDEX idx_flashcards_topic_id ON flashcards(topic_id);
CREATE INDEX idx_flashcards_subtopic_id ON flashcards(subtopic_id);

-- Response and session indexes
CREATE INDEX idx_mcq_responses_user_id ON mcq_user_responses(user_id);
CREATE INDEX idx_mcq_responses_mcq_id ON mcq_user_responses(mcq_id);
CREATE INDEX idx_sessions_user_id ON user_learning_sessions(user_id);
CREATE INDEX idx_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_flashcard_reviews_user_id ON flashcard_reviews(user_id);

-- Composite indexes for common queries
CREATE INDEX idx_user_topic_progress ON user_progress(user_id, topic_id) WHERE topic_id IS NOT NULL;
CREATE INDEX idx_user_subtopic_progress ON user_progress(user_id, subtopic_id) WHERE subtopic_id IS NOT NULL;
```

## Key Design Decisions

1. **Flexible Topic/Subtopic References**: MCQs and flashcards can be associated with either topics or subtopics, providing flexibility in content organization.

2. **Session-Based Tracking**: All user interactions are grouped into sessions, enabling comprehensive analytics and progress tracking.

3. **Difficulty Progression**: Built-in difficulty tracking and progression system for adaptive learning.

4. **Duplicate Prevention**: Hash-based duplicate detection for documents, MCQs, and content.

5. **Soft Deletes**: Using `is_active` flags instead of hard deletes to maintain data integrity and audit trails.

6. **Extensible Metadata**: JSONB fields for storing AI-generated metadata and future extensibility.

7. **Performance Optimization**: Strategic indexing for common query patterns and user interactions.