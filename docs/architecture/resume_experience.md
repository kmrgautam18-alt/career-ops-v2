# Resume Experience Intelligence

## Objective

Extract structured work experience from any resume and convert it into a normalized data model.

This module is domain-independent.

It must work for:

- Software Engineers
- DevOps Engineers
- Doctors
- Lawyers
- Teachers
- Students
- Freshers
- Designers
- Sales Professionals
- Finance Professionals
- Career Switchers

---

# Input

Normalized Resume Text

---

# Output

Structured Experience Objects

Example

[
    {
        "company": "HCLTech",
        "designation": "Azure Cloud Administrator",
        "employment_type": "Full Time",
        "location": "Noida",
        "start_date": "2023-05",
        "end_date": null,
        "currently_working": true,
        "duration_months": 26,
        "description": "...",
        "technologies": [
            "Azure",
            "Docker",
            "Kubernetes"
        ]
    }
]

---

# Responsibilities

Experience Extractor is responsible for:

- Company Detection
- Job Title Detection
- Employment Timeline
- Current Employer Detection
- Duration Calculation
- Responsibility Extraction
- Technology Extraction
- Achievement Extraction

---

# Non Responsibilities

Experience Extractor should NOT

- Save data into database
- Parse PDF
- Perform AI Matching
- Calculate Resume Score

---

# Architecture

Resume Upload

↓

Resume Parser

↓

Normalized Text

↓

Experience Extractor

↓

Experience Repository

↓

resume_experiences

---

# Future

Future versions will support

- AI Timeline Detection
- Company Knowledge Graph
- Organization Normalization
- Experience Confidence Score
- Multi-language Resume Parsing
- Cross-country Resume Formats
- Career Gap Detection
- Promotion Detection