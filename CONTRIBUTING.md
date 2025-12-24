# Contributing to PraisonAI Test

Thank you for your interest in contributing to PraisonAI Test! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🧪 Add tests
- 🔧 Fix bugs and implement features
- 🎨 Improve UI/UX

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/PraisonAI-Test.git
cd PraisonAI-Test
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 🔧 Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=praisonai_test --cov-report=html

# Run specific test file
pytest tests/test_agent_test.py -v

# Run specific test
pytest tests/test_agent_test.py::test_specific_function -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/

# Lint code
ruff check src/ tests/

# Fix linting issues
ruff check src/ tests/ --fix

# Type checking
mypy src/
```

### Testing Your Changes

```bash
# Test the CLI
praisonai-test --help
praisonai-test new test-suite
cd test-suite
praisonai-test run

# Test with examples
cd examples/basic-agent-test
praisonai-test run
```

## 📝 Code Style

### Python Style Guide

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use type hints where possible
- Write docstrings for all public functions/classes

### Example

```python
"""
Module description
"""

from typing import List, Optional


def example_function(param1: str, param2: int = 10) -> List[str]:
    """
    Brief description of function
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    
    Returns:
        List of strings
    
    Example:
        >>> example_function("test")
        ["result"]
    """
    result = []
    # Implementation
    return result
```

### Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(mocks): add support for Azure OpenAI mocking

fix(assertions): handle None values in assert_contains

docs(readme): update installation instructions

test(agent_test): add parametrize decorator tests
```

## 🧪 Testing Guidelines

### Writing Tests

1. **Test Organization**
   - Place tests in `tests/` directory
   - Name test files `test_*.py`
   - Use descriptive test names

2. **Test Structure**
   ```python
   def test_descriptive_name():
       # Arrange
       setup_data = "test"
       
       # Act
       result = function_to_test(setup_data)
       
       # Assert
       assert result == expected_value
   ```

3. **Coverage**
   - Aim for >80% code coverage
   - Test edge cases and error conditions
   - Test both success and failure paths

### Example Test

```python
"""Test agent_test module"""

import pytest
from praisonai_test import AgentTest, test_agent


def test_agent_test_creation():
    """Test AgentTest instance creation"""
    test = AgentTest()
    assert test is not None
    assert test.results == []


def test_assert_contains():
    """Test assert_contains assertion"""
    test = AgentTest()
    
    # Should pass
    test.assert_contains("hello world", "world")
    
    # Should fail
    with pytest.raises(AssertionError):
        test.assert_contains("hello world", "missing")
```

## 📚 Documentation

### Docstrings

Use Google-style docstrings:

```python
def function(arg1: str, arg2: int) -> bool:
    """
    Brief description
    
    Longer description if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When argument is invalid
    
    Example:
        >>> function("test", 10)
        True
    """
```

### README Updates

When adding features:
1. Update main README.md
2. Add examples
3. Update relevant documentation sections

## 🔄 Pull Request Process

### Before Submitting

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black src/ tests/`)
- [ ] Linting passes (`ruff check src/ tests/`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)

### Submitting PR

1. Push your changes to your fork
2. Create a pull request to `main` branch
3. Fill in the PR template
4. Link any related issues
5. Wait for review

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted
- [ ] Linting passes
```

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Step 1
2. Step 2
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Package version: [e.g., 0.1.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## 📋 Development Tasks

### High Priority
- [ ] Add more LLM provider mocks
- [ ] Implement async test support
- [ ] Add performance benchmarking
- [ ] Improve error messages

### Medium Priority
- [ ] Add more assertion helpers
- [ ] Create pytest plugin
- [ ] Add VS Code extension
- [ ] Improve HTML reports

### Low Priority
- [ ] Add CLI autocompletion
- [ ] Create interactive test creation
- [ ] Add test analytics

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Contact

- GitHub Issues: https://github.com/MervinPraison/PraisonAI-Test/issues
- Email: mervin@praison.ai
- Website: https://praison.ai

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to PraisonAI Test! 🎉

