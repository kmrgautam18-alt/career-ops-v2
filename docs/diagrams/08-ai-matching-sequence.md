# AI Matching & Career Intelligence Sequence

Version: 1.0

Status: Active

---

# Purpose

This diagram illustrates how the AI services process requests for ATS scoring, interview question generation, and resume optimization within Career-Ops v2.

---

# AI Service Architecture

```mermaid
flowchart TD

    Client["👤 User"]
    Frontend["⚛️ React Frontend"]
    Nginx["🌐 Nginx Proxy"]
    Router["📡 FastAPI Router"]
    AIService["🤖 AI Service Layer"]
    ATSEngine["📊 ATS Score Calculator"]
    InterviewEngine["🎤 Interview Generator"]
    Optimizer["📝 Resume Optimizer"]
    Matcher["🎯 Job Matcher"]
    Response["📦 ApiResponse"]

    Client --> Frontend
    Frontend --> Nginx
    Nginx --> Router
    Router --> AIService
    AIService --> ATSEngine
    AIService --> InterviewEngine
    AIService --> Optimizer
    AIService --> Matcher
    ATSEngine --> Response
    InterviewEngine --> Response
    Optimizer --> Response
    Matcher --> Response
```

---

# ATS Score Calculation

```mermaid
sequenceDiagram

actor User
participant Frontend as React Frontend
participant API as /api/v1/ai/ats-score
participant ATS as ATSEngine
participant Analyzer as KeywordAnalyzer
participant Formatter as FormattingAnalyzer
participant Section as SectionAnalyzer
participant Recommender as RecommendationBuilder

User->>Frontend: Pastes resume text + job description
Frontend->>API: POST /ai/ats-score {resume_text, job_description}
API->>ATS: calculate_ats_score(resume_text, job_description)

ATS->>Analyzer: analyze_keywords(resume, job_desc)
Analyzer-->>ATS: keyword_match_score, missing_keywords, matched_keywords

ATS->>Formatter: analyze_formatting(resume_text)
Formatter-->>ATS: formatting_score, issues

ATS->>Section: analyze_sections(resume_text)
Section-->>ATS: section_score, missing_sections

ATS->>ATS: calculate_weighted_score(keyword=40%, format=30%, section=30%)

ATS->>Recommender: build_recommendations(missing_keywords, format_issues, missing_sections)
Recommender-->>ATS: [{type: "keyword", message: "Add 'Python' skill"}, ...]

ATS-->>API: {score: 85, breakdown: {keywords: 80, formatting: 90, sections: 85}, recommendations: [...]}
API-->>Frontend: ApiResponse with results
Frontend-->>User: Display score with color gradient + recommendation list
```

---

# Interview Question Generation

```mermaid
sequenceDiagram

actor User
participant Frontend as React Frontend
participant API as /api/v1/ai/interview/questions
participant Service as InterviewService
participant Generator as QuestionGenerator
participant Difficulty as DifficultyEngine
participant Bank as QuestionBank

User->>Frontend: Enters job title, company, difficulty
Frontend->>API: POST /ai/interview/questions {job_title, company, difficulty}
API->>Service: generate_questions(job_title, company, difficulty)

Service->>Bank: get_template_questions(job_title)
Bank-->>Service: role-based question templates

Service->>Difficulty: adjust_difficulty(questions, "medium")
Difficulty-->>Service: difficulty-adjusted questions

Service->>Generator: generate_questions(templates, company_context)
Generator-->>Service: [{question: "Describe...", category: "Technical"}, ...]

Service-->>API: {questions: [{question: "...", category: "..."}, ...]}
API-->>Frontend: ApiResponse with questions
Frontend-->>User: Display numbered question cards
```

---

# Resume Optimization

```mermaid
sequenceDiagram

actor User
participant Frontend as React Frontend
participant API as /api/v1/ai/resume-optimize
participant Service as ResumeOptimizer
participant PromptBuilder as PromptBuilder
participant Recommender as RecommendationEngine

User->>Frontend: Pastes resume text + target job description
Frontend->>API: POST /ai/resume-optimize {resume_text, job_description}
API->>Service: optimize_resume(resume_text, job_description)

Service->>PromptBuilder: build_optimization_prompt(resume, job)
PromptBuilder-->>Service: structured prompt

Service->>Recommender: generate_recommendations(prompt)
Recommender-->>Service: [{section: "summary", suggestion: "Add...", priority: "high"}, ...]

Service-->>API: {optimized_sections: [...], recommendations: [...], match_score: 72}
API-->>Frontend: ApiResponse with optimization results
Frontend-->>User: Display suggestions with priority badges
```

---

# Job Matching

```mermaid
sequenceDiagram

actor User
participant Frontend as React Frontend
participant API as /api/v1/jobs/{job_id}/match/{resume_id}
participant Service as MatchService
participant Matchers as MatcherPipeline
participant Scorer as ScoreCalculator

User->>Frontend: Clicks "Match Job" on a job card
Frontend->>API: POST /jobs/1/match/1
API->>Service: match_job(job_id=1, resume_id=1, user_id=1)

Service->>Service: Verify resume ownership
Service->>Matchers: run_matchers(job, resume_data)

Matchers->>Matchers: skill_matcher()
Matchers->>Matchers: experience_matcher()
Matchers->>Matchers: education_matcher()
Matchers->>Matchers: keyword_matcher()
Matchers->>Matchers: location_matcher()

Matchers-->>Scorer: {skill: 85, experience: 70, education: 90, keyword: 75, location: 100}
Scorer->>Scorer: weighted_average(scores)
Scorer-->>Service: {overall: 82, breakdown: {...}, recommendations: [...]}

Service-->>API: ApiResponse with match results
API-->>Frontend: Display match score + detailed breakdown
Frontend-->>User: See match percentage + improvement tips
```

---

# AI Module Status

| Service | Endpoint | Status |
|---------|----------|:------:|
| ATS Score | `POST /api/v1/ai/ats-score` | ✅ |
| Interview Questions | `POST /api/v1/ai/interview/questions` | ✅ |
| Resume Optimization | `POST /api/v1/ai/resume-optimize` | ✅ |
| Job Matching | `POST /api/v1/jobs/{id}/match/{resume_id}` | ✅ |
