# Resume Engine Architecture

Version: 2.0

Status: Active

---

# Overview

The Resume Engine handles uploading, validating, storing, parsing, and managing user resumes. It includes AI-powered analysis, ATS scoring, and skill extraction.

---

# Resume Upload Flow

```mermaid
flowchart LR

    Client["👤 Authenticated User"]
    API["🌐 POST /api/v1/resumes/upload"]
    Validate["✅ File Validation
Type: PDF/DOCX
Size: Max 10MB"]
    Storage["💾 File Storage
Filesystem"]
    DB["🗄 Database Record
resumes table"]
    Parser["🔍 Resume Parser
PyMuPDF"]
    Profile["📋 Profile Extraction"]
    Experience["💼 Experience Extraction"]
    Skills["🔧 Skill Extraction"]
    Education["🎓 Education Extraction"]

    Client --> API
    API --> Validate
    Validate --> Storage
    Validate --> DB
    DB --> Parser
    Parser --> Profile
    Parser --> Experience
    Parser --> Skills
    Parser --> Education
```

---

# Resume Lifecycle

```mermaid
stateDiagram-v2

    [*] --> Uploaded
    Uploaded --> Validated
    Validated --> Stored
    Stored --> Parsed
    Parsed --> AIProcessed
    AIProcessed --> ReadyForMatching
    ReadyForMatching --> Matched
```

---

# Module Status

| Module | Status | Description |
|--------|--------|-------------|
| Upload API | ✅ | POST /api/v1/resumes/upload |
| File Validation | ✅ | PDF/DOCX type check, size limit |
| File Storage | ✅ | Filesystem storage with unique names |
| Database CRUD | ✅ | Create, read, update, delete resumes |
| Resume Download | ✅ | GET /api/v1/resumes/{id}/download |
| Resume Preview | ✅ | GET /api/v1/resumes/{id}/preview |
| Resume Listing | ✅ | GET /api/v1/resumes (paginated) |
| Profile Extraction | ✅ | Name, email, phone, location, summary |
| Experience Extraction | ✅ | Company, designation, dates, description |
| Skill Extraction | ✅ | Skills with categories and confidence |
| Education Extraction | ✅ | Degree, institution, dates, grades |
| Confidence Scoring | ✅ | Each extraction has a confidence score |
| ATS Scoring | ✅ | AI-powered resume vs job analysis |
| Resume Optimization | ✅ | AI-powered improvement suggestions |
| Job Matching | ✅ | Score resumes against job requirements |

---

# Storage Architecture

```
uploads/
└── resumes/
    └── {user_id}/
        └── {uuid}_{original_name}.pdf
```

- Files stored by user ID for isolation
- UUID prefixed to prevent name collisions
- Original name preserved for display
- Migration-ready for S3/GCS/Azure Blob

---

# Supported File Types

| Format | Support | Parser |
|--------|---------|--------|
| PDF | ✅ | PyMuPDF |
| DOCX | ✅ | python-docx (planned) |

---

# Extraction Pipeline

```mermaid
flowchart TD
    PDF["📄 Raw PDF"]
    Text["📝 Extracted Text"]
    ProfileExtract["Profile Extractor"]
    ExpExtract["Experience Extractor"]
    SkillExtract["Skill Extractor"]
    EduExtract["Education Extractor"]
    Knowledge["🧠 Knowledge Engine
Company DB · Skill Categories
Designations · Locations"]
    DBStore["🗄 Database Storage"]

    PDF --> Text
    Text --> ProfileExtract
    Text --> ExpExtract
    Text --> SkillExtract
    Text --> EduExtract
    Knowledge --> ProfileExtract
    Knowledge --> ExpExtract
    Knowledge --> SkillExtract
    Knowledge --> EduExtract
    ProfileExtract --> DBStore
    ExpExtract --> DBStore
    SkillExtract --> DBStore
    EduExtract --> DBStore
```

---

# Knowledge Base

The extraction engine uses a curated knowledge base stored in `backend/app/resources/`:

| Resource | Purpose |
|----------|---------|
| `companies/` | Known company names for matching |
| `designations/` | Common job titles and roles |
| `education/` | Degrees, institutions, specializations |
| `locations/` | Cities, states, countries |
| `skills/` | Skill categories (programming, cloud, DevOps, etc.) |
