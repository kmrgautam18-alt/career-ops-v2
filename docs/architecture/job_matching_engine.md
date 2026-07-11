# AI Job Matching Engine Architecture

Version: 1.0

---

# Overview

The Job Matching Engine is a stateless service responsible for calculating an explainable compatibility score between a parsed resume and a job posting.

The engine follows a modular architecture so that individual scoring components can evolve independently.

---

# High-Level Flow

Resume
        │
        ▼
Resume Repository
        │
        ▼
Resume Information
        │
        ▼
Job Repository
        │
        ▼
Job Matching Service
        │
        ├──────────────┐
        │              │
        ▼              ▼
Skill Matcher     Experience Matcher
        │              │
        ├──────────────┤
        ▼              ▼
Education Matcher  Certification Matcher
        │              │
        ├──────────────┤
        ▼              ▼
Location Matcher   Keyword Matcher
        │
        ▼
Score Calculator
        │
        ▼
Recommendation Engine
        │
        ▼
Explainability Engine
        │
        ▼
Match Result
```

---

# Core Components

## JobMatchingService

Responsibilities

- Load resume
- Load job
- Execute all matchers
- Aggregate results
- Return final result

No scoring logic should exist here.

---

## SkillMatcher

Responsibilities

- Exact matching
- Alias matching
- Category matching
- Related technology matching

Output

SkillMatchResult

---

## ExperienceMatcher

Responsibilities

Compare

- years
- designations
- domains

Output

ExperienceMatchResult

---

## EducationMatcher

Responsibilities

Compare

- degree
- specialization
- institution

Output

EducationMatchResult

---

## CertificationMatcher

Responsibilities

Compare required and preferred certifications.

---

## LocationMatcher

Responsibilities

Evaluate

- remote
- relocation
- country
- city

---

## KeywordMatcher

Responsibilities

Tokenize

Normalize

Calculate keyword similarity.

---

## ScoreCalculator

Responsibilities

Apply configurable weights.

Produce

Overall Score

---

## RecommendationEngine

Responsibilities

Generate

- strengths
- weaknesses
- missing skills
- recommendations

---

## ExplainabilityEngine

Responsibilities

Generate human-readable explanations for every score deduction and bonus.

---

# Configuration

Weights must not be hardcoded.

Future configuration source:

database

yaml

environment

---

# Extension Points

Future replacement modules

SkillMatcher

↓

EmbeddingSkillMatcher

KeywordMatcher

↓

LLMKeywordMatcher

RecommendationEngine

↓

CareerCoachAI

without changing the API.

---

# Performance

Target

<100ms

Stateless

Yes

Thread Safe

Yes

---

# Dependencies

Resume Repository

Job Repository

Knowledge Engine

Skill Extractor

Education Extractor

Experience Extractor

---

# API

POST

/api/v1/jobs/{job_id}/match

GET

/api/v1/jobs/{job_id}/match/details

GET

/api/v1/jobs/recommendations

---

# Future Architecture

Rule Engine

↓

Hybrid Engine

↓

Embedding Engine

↓

LLM Engine

↓

Personal Career Coach