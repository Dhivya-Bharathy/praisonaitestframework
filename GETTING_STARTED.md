# Getting Started with PraisonAI Test

This guide will help you get started with PraisonAI Test in 5 minutes.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Writing Your First Test](#writing-your-first-test)
4. [Running Tests](#running-tests)
5. [Understanding Mocks](#understanding-mocks)
6. [Next Steps](#next-steps)

## Installation

Install PraisonAI Test using pip:

```bash
pip install praisonai-test
```

Verify installation:

```bash
praisonai-test --version
```

## Quick Start

### 1. Create a New Test Suite

```bash
praisonai-test new my-first-test
cd my-first-test
```

This creates:
```
my-first-test/
├── test_agent.py       # Your test file
├── test_config.yaml    # Configuration
├── .env.example        # Environment template
├── conftest.py         # Pytest fixtures
└── README.md           # Instructions
```

### 2. Look at the Generated Test

Open `test_agent.py`:

```python
from praisonai_test import AgentTest, test_agent

class TestMyAgent(AgentTest):
    """Test suite for my AI agent"""
    
    def setup(self):
        """Setup before each test"""
        # Initialize your agent here
        pass
    
    @test_agent
    def test_simple_query(self):
        """Test basic agent query"""
        result = "This is a mock response"
        
        # Use assertions
        self.assert_contains(result, "mock")
        self.assert_not_contains(result, "error")
```

### 3. Run Your First Test

```bash
praisonai-test run
```

You should see:
```
Running AI Agent Tests

✅ TestMyAgent: 3 passed, 0 failed, 0 skipped

Test Summary
┏━━━━━━━━━┳━━━━━━━┓
┃ Status  ┃ Count ┃
┡━━━━━━━━━╇━━━━━━━┩
│ Passed  │     3 │
│ Failed  │     0 │
│ Skipped │     0 │
│ Total   │     3 │
│ Duration│ 0.15s │
└─────────┴───────┘

✅ All tests passed!
```

## Writing Your First Test

### Basic Test Structure

```python
from praisonai_test import AgentTest, test_agent

class TestMyAgent(AgentTest):
    """Describe what you're testing"""
    
    def setup(self):
        """Runs before each test"""
        # Setup code here
        pass
    
    @test_agent
    def test_something(self):
        """Test description"""
        # Your test code
        result = "agent output"
        
        # Assertions
        self.assert_contains(result, "expected")
```

### Example: Testing a Chatbot

```python
from praisonai_test import AgentTest, test_agent

class TestChatbot(AgentTest):
    """Test chatbot responses"""
    
    def setup(self):
        """Initialize chatbot"""
        # self.chatbot = MyChatbot()
        pass
    
    @test_agent
    def test_greeting(self):
        """Test chatbot greets users"""
        # Simulate response (replace with actual call)
        response = "Hello! How can I help you today?"
        
        # Check response contains greeting
        self.assert_contains(response, "Hello", case_sensitive=False)
        self.assert_contains(response, "help")
    
    @test_agent
    def test_farewell(self):
        """Test chatbot says goodbye"""
        response = "Goodbye! Have a great day!"
        
        self.assert_contains(response, "Goodbye", case_sensitive=False)
        self.assert_not_contains(response, "error")
    
    @test_agent
    def test_response_time(self):
        """Test chatbot responds quickly"""
        import time
        
        start = time.time()
        # response = self.chatbot.chat("Hello")
        duration = time.time() - start
        
        # Assert responds within 2 seconds
        self.assert_latency(duration, max_seconds=2.0)
```

## Running Tests

### Basic Commands

```bash
# Run all tests
praisonai-test run

# Verbose output
praisonai-test run -v

# Run specific directory
praisonai-test run --path tests/

# Run specific file
praisonai-test run-file test_agent.py
```

### Generate Reports

```bash
# HTML report
praisonai-test run --report html --output report.html

# JSON report
praisonai-test run --report json --output report.json

# JUnit XML (for CI/CD)
praisonai-test run --report junit --output junit.xml
```

### Using Pytest Directly

```bash
# Standard pytest
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test
pytest tests/test_agent.py::TestMyAgent::test_something -v
```

## Understanding Mocks

Mocks let you test without making real API calls (save money!).

### Why Use Mocks?

- ✅ **Fast** - No network calls
- ✅ **Free** - No API costs
- ✅ **Reliable** - No API downtime
- ✅ **Reproducible** - Same results every time

### Basic Mocking

```python
from praisonai_test import AgentTest, test_agent, MockLLM, mock_llm_response

class TestWithMock(AgentTest):
    """Test using mocks"""
    
    def setup(self):
        """Setup mock LLM"""
        self.mock = MockLLM()
        
        # Add a response
        self.mock.add_response(
            "What is 2+2?",
            mock_llm_response("The answer is 4", tokens_used=20)
        )
    
    @test_agent
    def test_with_mock(self):
        """Test using mock response"""
        result = self.mock.get_response("What is 2+2?")
        
        self.assert_contains(result.content, "4")
        assert result.tokens_used == 20
```

### Pattern-Based Mocking

```python
def setup(self):
    self.mock = MockLLM()
    
    # Match any question about capitals
    self.mock.add_pattern(
        r".*capital.*",
        "That's a geography question"
    )

@test_agent
def test_pattern_match(self):
    result = self.mock.get_response("What is the capital of France?")
    self.assert_contains(result.content, "geography")
```

### Function-Based Mocking

```python
def setup(self):
    self.mock = MockLLM()
    
    # Custom matching logic
    def is_math_question(prompt, **kwargs):
        return any(op in prompt for op in ['+', '-', '*', '/'])
    
    self.mock.add_function_response(
        is_math_question,
        "This is a math question"
    )

@test_agent
def test_math_detection(self):
    result = self.mock.get_response("What is 10 * 5?")
    self.assert_contains(result.content, "math")
```

## Common Assertions

### Content Assertions

```python
# Check if text contains something
self.assert_contains(output, "expected text")

# Check if text doesn't contain something
self.assert_not_contains(output, "error")

# Check exact equality
self.assert_equals(actual, expected)

# Check semantic similarity
self.assert_similarity(output, "expected meaning", min_score=0.8)
```

### Format Assertions

```python
# Validate JSON
self.assert_json_valid('{"key": "value"}')

# Check format
from praisonai_test.assertions import assert_format
assert_format(output, "json")     # json, yaml, markdown, html, xml
```

### Performance Assertions

```python
# Check response time
self.assert_latency(duration, max_seconds=2.0)

# Check cost
self.assert_cost(cost, max_cost=0.10)

# Check token usage
from praisonai_test.assertions import assert_token_count
assert_token_count(tokens, max_tokens=1000)
```

### Safety Assertions

```python
from praisonai_test.assertions import assert_no_pii, assert_no_hallucination

# Check for PII leakage
assert_no_pii(output)

# Check for hallucinations
source_docs = ["Source document 1", "Source document 2"]
assert_no_hallucination(output, source_docs, threshold=0.7)
```

## Next Steps

### 1. Explore Examples

```bash
# Clone the repository
git clone https://github.com/MervinPraison/PraisonAI-Test.git
cd PraisonAI-Test

# Run examples
cd examples/basic-agent-test
praisonai-test run

cd ../mock-llm-test
praisonai-test run
```

### 2. Add to Existing Project

```bash
# In your project directory
praisonai-test init

# This creates:
# - tests/ directory
# - Example test file
# - pytest.ini configuration
```

### 3. Set Up CI/CD

Add to `.github/workflows/test.yml`:

```yaml
name: Test AI Agents

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: pip install praisonai-test
    - run: praisonai-test run --report junit --output junit.xml
```

### 4. Learn More

- **Documentation**: https://mervinpraison.github.io/PraisonAI-Test
- **Examples**: `examples/` directory
- **API Reference**: See docstrings in source code
- **Issues**: https://github.com/MervinPraison/PraisonAI-Test/issues

## Tips & Best Practices

### 1. Organize Tests by Feature

```
tests/
├── test_chatbot.py          # Chatbot tests
├── test_summarization.py    # Summarization tests
├── test_analysis.py         # Analysis tests
└── conftest.py              # Shared fixtures
```

### 2. Use Descriptive Test Names

```python
# Good
def test_chatbot_greets_user_with_name(self):
    pass

# Bad
def test_1(self):
    pass
```

### 3. Test One Thing Per Test

```python
# Good - focused test
@test_agent
def test_greeting_includes_name(self):
    response = self.bot.greet("Alice")
    self.assert_contains(response, "Alice")

@test_agent
def test_greeting_is_polite(self):
    response = self.bot.greet("Alice")
    self.assert_contains(response, "please")

# Bad - testing multiple things
@test_agent
def test_greeting(self):
    response = self.bot.greet("Alice")
    self.assert_contains(response, "Alice")
    self.assert_contains(response, "please")
    self.assert_latency(duration, max_seconds=1.0)
```

### 4. Use Setup and Teardown

```python
class TestMyAgent(AgentTest):
    def setup(self):
        """Initialize resources"""
        self.agent = MyAgent()
        self.test_data = load_test_data()
    
    def teardown(self):
        """Clean up resources"""
        self.agent.cleanup()
```

### 5. Mock by Default, Test Real Occasionally

- Use mocks for unit tests (fast, reliable)
- Use real APIs for integration tests (scheduled, less frequent)
- Use environment variables to switch:

```python
import os

def setup(self):
    if os.getenv("USE_REAL_API") == "true":
        self.llm = RealLLM()
    else:
        self.llm = MockLLM()
```

## Troubleshooting

### Tests Not Found

```bash
# Make sure you're in the right directory
praisonai-test run --path tests/

# Or use pytest directly
pytest -v
```

### Import Errors

```bash
# Reinstall package
pip install -e ".[dev]"

# Or install from PyPI
pip install --upgrade praisonai-test
```

### Assertion Failures

Check the detailed error message:
- What was expected?
- What was actual?
- Review your test logic

## Get Help

- **Issues**: https://github.com/MervinPraison/PraisonAI-Test/issues
- **Discussions**: https://github.com/MervinPraison/PraisonAI-Test/discussions
- **Email**: mervin@praison.ai

---

Happy Testing! 🧪✨

