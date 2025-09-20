# Contributing to Land Opportunity Search

Thank you for your interest in contributing to Land Opportunity Search! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- Docker & Docker Compose
- Basic understanding of Reinforcement Learning and FastAPI

### Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/landOpSearch.git
cd landOpSearch
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install development dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

4. **Set up pre-commit hooks**
```bash
pre-commit install
```

## 🛠️ Development Guidelines

### Code Style

We follow these coding standards:

- **Python**: PEP 8 with Black formatting
- **Type Hints**: Required for all functions and methods
- **Docstrings**: Google-style docstrings for all public APIs
- **Comments**: Clear, concise comments for complex logic

### Project Structure

```
land-agent-backend/
├── env_service/          # RL environment
├── trainer/             # Model training
├── inference_api/       # FastAPI service
├── data_ingestion/      # Data pipeline
├── airflow/            # Workflow orchestration
├── k8s/                # Kubernetes configs
├── infra/              # Infrastructure
├── tests/              # Test suite
└── docs/               # Documentation
```

### Branch Naming

Use descriptive branch names with prefixes:

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements

Examples:
- `feature/satellite-integration`
- `bugfix/api-response-validation`
- `docs/api-documentation`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run tests with verbose output
pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

Example test structure:
```python
import pytest
from unittest.mock import Mock, patch

class TestLandOpportunityEnv:
    def test_environment_initialization(self):
        """Test environment initializes correctly."""
        env = LandOpportunityEnv(land_data={})
        assert env.current_step == 0
        assert env.max_steps == 100
    
    def test_step_function_returns_correct_format(self):
        """Test step function returns proper tuple."""
        env = LandOpportunityEnv(land_data={})
        state = env.reset()
        action = 0
        next_state, reward, done, info = env.step(action)
        
        assert isinstance(next_state, np.ndarray)
        assert isinstance(reward, float)
        assert isinstance(done, bool)
        assert isinstance(info, dict)
```

## 📝 Documentation

### Code Documentation

- Use Google-style docstrings
- Include type hints for all parameters and return values
- Document complex algorithms and business logic
- Provide usage examples for public APIs

Example:
```python
async def evaluate_land(self, data: LandData) -> EvaluationResponse:
    """
    Evaluate a land parcel using the trained model.
    
    Args:
        data: Land data containing features for evaluation
        
    Returns:
        Evaluation response with score, confidence, and recommended action
        
    Raises:
        HTTPException: If model is not loaded or evaluation fails
        
    Example:
        >>> data = LandData(features=[0.5, 0.6, 0.8, 0.3, 0.2, 0.9, 0.7, 0.4, 0.6])
        >>> response = await evaluate_land(data)
        >>> print(response.score)
        0.75
    """
```

### API Documentation

- Update OpenAPI specifications for API changes
- Include request/response examples
- Document error codes and messages
- Maintain changelog for breaking changes

## 🔄 Pull Request Process

### Before Submitting

1. **Run tests**: Ensure all tests pass
2. **Check code quality**: Run linting and formatting
3. **Update documentation**: Update relevant docs
4. **Write clear commit messages**: Use conventional commits

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)

## Screenshots (if applicable)
Add screenshots for UI changes

## Additional Notes
Any additional information for reviewers
```

### Review Process

1. **Automated checks**: CI/CD pipeline runs tests and linting
2. **Code review**: At least one maintainer reviews the PR
3. **Testing**: Manual testing if required
4. **Approval**: Maintainer approves and merges

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Ensure you're using the latest version
3. Try to reproduce the issue

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.10.0]
- Package version: [e.g. 0.1.0]

**Additional Context**
Any other context about the problem
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other solutions you've considered

**Additional Context**
Any other context or screenshots
```

## 🏗️ Architecture Decisions

### Making Changes

When proposing significant changes:

1. **Create an Architecture Decision Record (ADR)**
2. **Discuss in GitHub Discussions**
3. **Get approval from maintainers**
4. **Document the decision**

### ADR Template

```markdown
# ADR-XXX: Title

## Status
Proposed / Accepted / Rejected / Deprecated

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing?

## Consequences
What becomes easier or more difficult to do because of this change?
```

## 🔧 Development Tools

### Recommended IDE Setup

**VS Code Extensions:**
- Python
- Pylance
- Black Formatter
- isort
- GitLens
- Docker

**PyCharm:**
- Enable Black formatter
- Configure type checking
- Set up debugger for FastAPI

### Useful Commands

```bash
# Format code
black .
isort .

# Lint code
flake8 .
mypy .

# Security check
bandit -r .

# Run pre-commit hooks
pre-commit run --all-files

# Update dependencies
pip-compile requirements.in
pip-compile requirements-dev.in
```

## 📊 Performance Guidelines

### Code Performance

- Use async/await for I/O operations
- Implement proper caching strategies
- Optimize database queries
- Profile code for bottlenecks

### Model Performance

- Monitor model accuracy and drift
- Implement A/B testing for model updates
- Use proper evaluation metrics
- Document performance baselines

## 🛡️ Security Guidelines

### Security Best Practices

- Never commit secrets or API keys
- Use environment variables for configuration
- Implement proper input validation
- Follow OWASP guidelines
- Regular dependency updates

### Reporting Security Issues

For security vulnerabilities, please email security@landopsearch.com instead of creating a public issue.

## 📞 Getting Help

### Community Support

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Discord**: Join our community server
- **Email**: dev@landopsearch.com

### Maintainers

- [@maintainer1](https://github.com/maintainer1) - Lead Developer
- [@maintainer2](https://github.com/maintainer2) - ML Engineer
- [@maintainer3](https://github.com/maintainer3) - DevOps Engineer

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at conduct@landopsearch.com.

---

Thank you for contributing to Land Opportunity Search! 🚀