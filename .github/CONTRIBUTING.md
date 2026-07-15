# Contributing to Career-Ops v2

First off, thank you for considering contributing! 🎉

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### 🐛 Reporting Bugs

1. Check if the bug already exists in [Issues](https://github.com/kmrgautam18-alt/career-ops-v2/issues)
2. If not, [create a new issue](https://github.com/kmrgautam18-alt/career-ops-v2/issues/new) with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)

### 💡 Suggesting Features

1. Check [existing issues](https://github.com/kmrgautam18-alt/career-ops-v2/issues) for similar suggestions
2. [Open a feature request](https://github.com/kmrgautam18-alt/career-ops-v2/issues/new) with:
   - Clear use case
   - Proposed solution
   - Alternatives considered

### 🚀 Pull Requests

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Make your changes following our coding conventions
4. Run tests:
   ```bash
   python3 -m pytest tests/ -q
   cd frontend && bun tsc -b --noEmit
   ```
5. Commit with clear messages:
   ```bash
   git commit -m 'feat: add amazing feature'
   ```
6. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
7. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2

# Backend
pip install -r requirements.txt
DATABASE_URL='sqlite:///./data/careerops.db' uvicorn backend.app.main:app --reload

# Frontend (separate terminal)
cd frontend
bun install
bun dev
```

## Coding Conventions

### Python
- Follow PEP 8 with Black formatter (88 chars)
- Type hints required for all functions
- Use Ruff for linting
- Write tests for new features

### TypeScript / React
- Functional components with hooks
- Explicit TypeScript types (no `any`)
- Tailwind CSS for styling
- Framer Motion for animations

## Architecture

- **Layered**: Router → Service → Repository → ORM → DB
- **Auth**: JWT tokens via `get_current_user()` dependencies
- **API**: RESTful with `ApiResponse` envelope `{success, message, data, pagination}`

## Need Help?

Open a [discussion](https://github.com/kmrgautam18-alt/career-ops-v2/discussions) or reach out to the maintainer.

Thank you for contributing! ❤️
