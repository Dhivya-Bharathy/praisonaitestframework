# PraisonAI Test 🧪

[![PyPI version](https://badge.fury.io/py/praisonai-test.svg)](https://badge.fury.io/py/praisonai-test)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Testing framework for AI agents with automated validation, mocking, and CI/CD integration**

Think `pytest` but specifically designed for AI agent workflows. PraisonAI Test completes the development cycle: **build → test → deploy → measure**.

## 🎯 Overview

PraisonAI Test fills the gap between development and deployment:

- **PraisonAI** - Build AI agents
- **PraisonAI-Test** - Test your agents (this framework) ⭐
- **PraisonAI-SVC** - Deploy to production
- **PraisonAIBench** - Benchmark performance

## ✨ Features

### Core Testing Capabilities
- ✅ **Simple Test Syntax** - Decorator-based testing similar to pytest
- ✅ **LLM Mocking** - Test without real API calls (save costs!)
- ✅ **Rich Assertions** - Specialized assertions for AI outputs
- ✅ **Performance Testing** - Latency, cost, and token tracking
- ✅ **Safety Validation** - PII detection, hallucination checks

### Developer Experience
- 🚀 **CLI Tools** - Create, run, and report on tests
- 📊 **Multiple Report Formats** - Console, JSON, HTML, JUnit
- 🔄 **CI/CD Ready** - GitHub Actions, GitLab CI templates included
- 🎨 **Beautiful Output** - Rich terminal UI with colors and tables

### LLM Provider Support
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Azure OpenAI
- LiteLLM (100+ providers)

## 🚀 Quick Start

### Installation

```bash
pip install praisonai-test
```

### Create Your First Test

```bash
# Create a new test suite
praisonai-test new my-agent-tests

# Navigate to the directory
cd my-agent-tests

# Configure environment (optional, uses mocks by default)
cp .env.example .env
```

### Write a Test

```python
# test_agent.py
from praisonai_test import AgentTest, test_agent

class TestMyAgent(AgentTest):
    """Test suite for my AI agent"""
    
    @test_agent
    def test_simple_query(self):
        """Test agent can answer basic questions"""
        # Your agent call here
        result = "The answer is 42"
        
        # Use rich assertions
        self.assert_contains(result, "42")
        self.assert_not_contains(result, "error")
```

### Run Tests

```bash
# Run all tests
praisonai-test run

# Generate HTML report
praisonai-test run --report html --output report.html

# Run specific file
praisonai-test run-file test_agent.py
```

## 📖 Documentation

### Writing Tests

#### Basic Test Structure

```python
from praisonai_test import AgentTest, test_agent

class TestMyAgent(AgentTest):
    def setup(self):
        """Run before each test"""
        # Initialize your agent
        self.agent = MyAgent()
    
    def teardown(self):
        """Run after each test"""
        # Cleanup
        pass
    
    @test_agent
    def test_something(self):
        """Test description"""
        result = self.agent.run("test query")
        self.assert_contains(result, "expected")
```

#### Using Decorators

```python
from praisonai_test import test_agent, skip_test, parametrize

# Skip a test
@skip_test("Not implemented yet")
@test_agent
def test_future_feature(self):
    pass

# Parametrized testing
@parametrize([
    {"input": "2+2", "expected": "4"},
    {"input": "3+3", "expected": "6"},
])
@test_agent
def test_math(self, input, expected):
    result = self.agent.run(input)
    self.assert_contains(result, expected)
```

### Assertions

#### Content Assertions

```python
# Contains/not contains
self.assert_contains(output, "expected text")
self.assert_not_contains(output, "unwanted text")

# Equality
self.assert_equals(actual, expected)

# Similarity (semantic matching)
self.assert_similarity(output, "expected meaning", min_score=0.8)
```

#### Format Assertions

```python
# JSON validation
self.assert_json_valid(output)

# Format checking
from praisonai_test.assertions import assert_format
assert_format(output, "json")  # json, yaml, markdown, html, xml
```

#### Performance Assertions

```python
# Latency
self.assert_latency(duration, max_seconds=5.0)

# Cost
self.assert_cost(cost, max_cost=0.10)

# Token count
from praisonai_test.assertions import assert_token_count
assert_token_count(tokens, max_tokens=1000)
```

#### Safety Assertions

```python
from praisonai_test.assertions import assert_no_pii, assert_no_hallucination

# PII detection
assert_no_pii(output)

# Hallucination checking
source_docs = ["document 1", "document 2"]
assert_no_hallucination(output, source_docs, threshold=0.7)
```

### LLM Mocking

#### Basic Mocking

```python
from praisonai_test import MockLLM, mock_llm_response

# Create mock
mock = MockLLM()

# Add exact match response
mock.add_response(
    "What is 2+2?",
    mock_llm_response("The answer is 4", tokens_used=20, cost=0.001)
)

# Add pattern-based response
mock.add_pattern(
    r".*capital.*",
    "I can help with geography"
)

# Get response
response = mock.get_response("What is 2+2?")
print(response.content)  # "The answer is 4"
print(response.tokens_used)  # 20
```

#### Provider-Specific Mocking

```python
# Use pytest fixtures
def test_with_openai(mock_openai):
    """Test with mocked OpenAI"""
    mock_openai.add_response("test", "response")
    
    # Your OpenAI calls will use the mock
    # No real API calls made!
    result = mock_openai.get_response("test")
    assert result.content == "response"
```

#### Advanced Mocking

```python
# Function-based matching
def is_math_question(prompt, **kwargs):
    return any(op in prompt for op in ['+', '-', '*', '/'])

mock.add_function_response(
    is_math_question,
    "This is a math question"
)

# Default response
mock.set_default_response("I don't know")

# Track calls
assert mock.get_call_count() == 5
last_call = mock.get_last_call()
```

### CLI Commands

#### `praisonai-test new`

Create a new test suite:

```bash
praisonai-test new my-tests
praisonai-test new my-tests --agent-type custom
```

#### `praisonai-test run`

Run tests:

```bash
# Run all tests
praisonai-test run

# Verbose output
praisonai-test run -v

# Specific path
praisonai-test run --path tests/

# Generate report
praisonai-test run --report html --output report.html
praisonai-test run --report junit --output junit.xml
```

#### `praisonai-test init`

Initialize testing in existing project:

```bash
praisonai-test init
```

Creates:
- `tests/` directory
- Example test file
- `pytest.ini` configuration
- `conftest.py` for fixtures

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: AI Agent Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install praisonai-test
    
    - name: Run tests
      env:
        MOCK_ENABLED: true  # Use mocks, no API keys needed
      run: |
        praisonai-test run --report junit --output junit.xml
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: junit.xml
```

### GitLab CI

See `.gitlab-ci.yml` in the repository for a complete example.

## 📊 Reporting

### Console Report

Default colorful terminal output with tables and summaries.

### HTML Report

```bash
praisonai-test run --report html --output report.html
```

Beautiful HTML report with:
- Summary dashboard
- Individual test results
- Error details
- Duration tracking

### JSON Report

```bash
praisonai-test run --report json --output report.json
```

Machine-readable format for further processing.

### JUnit XML

```bash
praisonai-test run --report junit --output junit.xml
```

Standard format for CI/CD systems.

## 🎯 Use Cases

### Unit Testing AI Agents

```python
class TestChatbot(AgentTest):
    @test_agent
    def test_greeting(self):
        result = self.agent.chat("Hello")
        self.assert_contains(result, "hi", case_sensitive=False)
```

### Integration Testing

```python
class TestAgentWorkflow(AgentTest):
    @test_agent
    def test_complete_workflow(self):
        # Step 1: Initialize
        self.agent.setup()
        
        # Step 2: Process
        result = self.agent.run("complex task")
        
        # Step 3: Validate
        self.assert_json_valid(result)
        self.assert_contains(result, "success")
```

### Performance Testing

```python
class TestPerformance(AgentTest):
    @test_agent
    def test_response_time(self):
        import time
        start = time.time()
        result = self.agent.run("query")
        duration = time.time() - start
        
        self.assert_latency(duration, max_seconds=2.0)
```

### Safety Testing

```python
class TestSafety(AgentTest):
    @test_agent
    def test_no_data_leakage(self):
        result = self.agent.run("query with user data")
        
        from praisonai_test.assertions import assert_no_pii
        assert_no_pii(result)
```

## 🏗️ Project Structure

```
praisonai-test/
├── src/praisonai_test/
│   ├── __init__.py          # Main exports
│   ├── agent_test.py        # AgentTest class
│   ├── mocks.py             # LLM mocking
│   ├── assertions.py        # Assertion helpers
│   ├── fixtures.py          # Pytest fixtures
│   ├── runner.py            # Test runner
│   ├── reporter.py          # Report generation
│   └── cli.py               # CLI commands
├── examples/
│   ├── basic-agent-test/    # Basic examples
│   └── mock-llm-test/       # Mocking examples
├── tests/                   # Framework tests
├── .github/workflows/       # CI/CD templates
├── pyproject.toml
└── README.md
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🔗 Related Projects

- **PraisonAI** - Build AI agents: https://github.com/MervinPraison/PraisonAI
- **PraisonAI-SVC** - Deploy agents: https://github.com/MervinPraison/PraisonAI-SVC
- **PraisonAIBench** - Benchmark agents: https://github.com/MervinPraison/PraisonAIBench

## 💡 Support

- **Documentation**: https://mervinpraison.github.io/PraisonAI-Test
- **Issues**: https://github.com/MervinPraison/PraisonAI-Test/issues
- **Website**: https://praison.ai

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ by the PraisonAI Team**

