# AI Job Matching Engine Requirements

Version: 1.0
Status: Draft
Owner: Career-Ops Backend
Priority: High

---

# 1. Overview

## Purpose

The AI Job Matching Engine compares a parsed resume with a job posting and calculates an explainable compatibility score.

The engine must produce deterministic results while remaining extensible for future AI and Machine Learning enhancements.

The first version will use rule-based scoring.

Future versions may use embeddings and Large Language Models without changing the external API.

---

# 2. Business Goal

Help job seekers understand:

- How well they match a job
- Why they received that score
- Which skills are missing
- Which strengths improve their profile
- What they should learn next

The engine should enable users to prioritize the most relevant jobs before applying.

---

# 3. Scope

Version 1 includes:

✓ Resume matching

✓ Skill comparison

✓ Experience comparison

✓ Education comparison

✓ Certification comparison

✓ Location comparison

✓ Explainable scoring

✓ Recommendation generation

Version 1 excludes:

× Salary prediction

× Company culture matching

× Personality analysis

× Interview probability

× Semantic AI

---

# 4. Functional Requirements

## FR-001

The engine shall compare a resume against one job.

---

## FR-002

The engine shall calculate a score between

0 and 100.

---

## FR-003

The engine shall calculate component scores.

Required components:

- Skill Score
- Experience Score
- Education Score
- Certification Score
- Location Score
- Keyword Score

---

## FR-004

The engine shall generate explanations.

Example:

Matched Skills:

Docker

Linux

Git

Missing Skills:

Terraform

Kubernetes

Azure DevOps

---

## FR-005

The engine shall classify the result.

Excellent Match

Strong Match

Moderate Match

Weak Match

Poor Match

---

## FR-006

The engine shall recommend improvements.

Example:

Learn Kubernetes

Add Terraform projects

Increase cloud experience

---

## FR-007

The engine shall detect missing required skills.

---

## FR-008

The engine shall identify resume strengths.

---

## FR-009

The engine shall identify over-qualified candidates.

---

## FR-010

The engine shall detect under-qualified candidates.

---

# 5. Inputs

Resume

Profile

Skills

Education

Experience

Certifications

Location

Projects

Job

Title

Description

Required Skills

Preferred Skills

Experience

Education

Location

Certifications

Keywords

---

# 6. Outputs

Overall Score

Classification

Matched Skills

Missing Skills

Extra Skills

Experience Gap

Education Gap

Certification Gap

Strengths

Weaknesses

Recommendations

Confidence

Processing Time

---

# 7. Weight Configuration

Skills

50%

Experience

20%

Education

10%

Keywords

10%

Certification

5%

Location

5%

Total

100%

Weights must be configurable.

---

# 8. Skill Matching Rules

Exact match

100%

Alias match

95%

Category match

70%

Related technology

50%

No match

0%

Example

Docker

Containerization

Partial Match

---

# 9. Experience Matching

Required

5 years

Candidate

6 years

Full score

Required

5 years

Candidate

3 years

Partial score

---

# 10. Education Matching

Higher degree

Full score

Equal degree

Full score

Lower degree

Partial score

No degree

Zero score

---

# 11. Certification Matching

Required certification

Present

Full score

Preferred certification

Present

Bonus

---

# 12. Location Matching

Same city

100

Remote

100

Same country

75

Different country

50

Relocation required

40

---

# 13. Keyword Matching

Tokenize

Normalize

Remove stop words

Calculate similarity

---

# 14. Explainability

Every score must include reasons.

Example

Matched:

Linux

Git

Docker

Missing:

Terraform

Azure

Reason

Missing required cloud technologies.

---

# 15. Recommendation Rules

90–100

Excellent Match

80–89

Strong Match

65–79

Moderate Match

50–64

Weak Match

Below 50

Poor Match

---

# 16. Performance

Target response

<100 ms

Memory

Minimal

Stateless

Yes

Thread Safe

Yes

---

# 17. Security

User isolation

Input validation

Authorization

No sensitive logging

---

# 18. Logging

Processing time

Final score

Errors

Warnings

Skipped components

---

# 19. API Requirements

Future endpoint

POST

/api/v1/jobs/{id}/match

Response

{
  "overall_score": 86,
  "classification": "Strong Match",
  "matched_skills": [],
  "missing_skills": [],
  "recommendations": []
}

---

# 20. Future AI Extensions

Vector Search

Embeddings

LLM Explanation

ATS Compatibility

Learning Roadmap

Salary Prediction

Interview Success Prediction

Resume Optimization

Career Coach

---

# 21. Acceptance Criteria

✓ Deterministic scoring

✓ Repeatable results

✓ Explainable output

✓ Unit tested

✓ Integration tested

✓ Performance under target

✓ No database schema changes required

---

# 22. Risks

Incomplete resumes

Poor job descriptions

Unknown technologies

Synonyms

Abbreviations

---

# 23. Out of Scope

Recruiter ranking

Behavior analysis

Personality matching

Psychometric analysis

Video interview analysis

---

# 24. References

Resume Parser

Knowledge Engine

Skill Extractor

Education Extractor

Experience Extractor