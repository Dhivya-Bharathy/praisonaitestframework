# PraisonAI Test - Project Structure

Complete overview of the PraisonAI Test framework structure and components.

## 📁 Directory Structure

```
praisonai-test/
│
├── src/praisonai_test/           # Main package
│   ├── __init__.py               # Package exports and version
│   ├── agent_test.py             # Core AgentTest class
│   ├── mocks.py                  # LLM mocking system
│   ├── assertions.py             # Assertion helpers
│   ├── fixtures.py               # Pytest fixtures
│   ├── runner.py                 # Test runner
│   ├── reporter.py               # Report generation
│   └── cli.py                    # Command-line interface
│
├── tests/                        # Framework tests
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_agent_test.py        # AgentTest tests
│   ├── test_mocks.py             # Mocking system tests
│   └── test_assertions.py        # Assertion tests
│
├── examples/                     # Example test suites
│   ├── __init__.py
│   ├── basic-agent-test/         # Basic examples
│   │   └── test_basic_agent.py
│   └── mock-llm-test/            # Mocking examples
│       └── test_with_mocks.py
│
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions CI/CD
│
├── .gitlab-ci.yml                # GitLab CI/CD
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Package configuration
├── pytest.ini                    # Pytest configuration
│
├── README.md                     # Main documentation
├── GETTING_STARTED.md            # Quick start guide
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
├── LICENSE                       # MIT License
└── PROJECT_STRUCTURE.md          # This file
```

## 🎯 Core Components

### 1. `agent_test.py` - Core Testing Framework

**Classes:**
- `AgentTest` - Base class for all agent tests
- `TestResult` - Dataclass for test results

**Decorators:**
- `@test_agent` - Mark methods as tests
- `@skip_test` - Skip tests
- `@parametrize` - Parametrized testing

**Key Methods:**
- `setup()` - Pre-test initialization
- `teardown()` - Post-test cleanup
- `run_test()` - Execute a test
- `assert_*()` - Various assertion methods

### 2. `mocks.py` - LLM Mocking System

**Classes:**
- `MockLLM` - Main mock LLM class
- `MockResponse` - Mock response dataclass
- `OpenAIMock` - OpenAI API mock
- `AnthropicMock` - Anthropic API mock
- `LiteLLMMock` - LiteLLM mock

**Features:**
- Exact prompt matching
- Pattern-based matching (regex)
- Function-based matching
- Call history tracking
- Default responses

### 3. `assertions.py` - Assertion Helpers

**Content Assertions:**
- `assert_contains()` - Check text contains substring
- `assert_not_contains()` - Check text doesn't contain substring
- `assert_agent_response()` - Flexible response validation

**Format Assertions:**
- `assert_json_valid()` - Validate JSON
- `assert_format()` - Validate format (json, yaml, markdown, html, xml)

**Performance Assertions:**
- `assert_latency()` - Check response time
- `assert_cost()` - Check API cost
- `assert_token_count()` - Check token usage

**Safety Assertions:**
- `assert_no_pii()` - Detect PII leakage
- `assert_no_hallucination()` - Check grounding in sources

**List Assertions:**
- `assert_list_length()` - Validate list length
- `assert_all_items_match()` - Pattern matching all items
- `assert_any_item_matches()` - Pattern matching any item

### 4. `fixtures.py` - Pytest Integration

**Fixtures:**
- `mock_llm` - MockLLM instance
- `mock_openai` - Mocked OpenAI client
- `mock_anthropic` - Mocked Anthropic client
- `mock_litellm` - Mocked LiteLLM
- `agent_fixture` - Decorator for agent fixtures
- `temp_config` - Temporary config directory
- `reset_environment` - Reset env vars

### 5. `runner.py` - Test Runner

**Class: `TestRunner`**

**Methods:**
- `discover_tests()` - Find test files and classes
- `run_all()` - Run all discovered tests
- `run_file()` - Run specific file
- `run_test()` - Run specific test

**Features:**
- Auto-discovery of test files
- Progress tracking with Rich
- Parallel test execution
- Summary generation

### 6. `reporter.py` - Report Generation

**Class: `TestReporter`**

**Report Formats:**
- Console - Rich terminal output
- JSON - Machine-readable format
- HTML - Beautiful web report
- JUnit XML - CI/CD integration

**Methods:**
- `generate_report()` - Generate report in any format
- `_report_console()` - Console output
- `_report_json()` - JSON output
- `_report_html()` - HTML output
- `_report_junit()` - JUnit XML output

### 7. `cli.py` - Command-Line Interface

**Commands:**
- `praisonai-test new` - Create new test suite
- `praisonai-test run` - Run tests
- `praisonai-test run-file` - Run specific file
- `praisonai-test report` - Generate report
- `praisonai-test init` - Initialize in existing project
- `praisonai-test version` - Show version

## 🔧 Configuration Files

### `pyproject.toml`

Main package configuration:
- Package metadata
- Dependencies
- Build system
- Entry points (CLI)
- Tool configurations (black, ruff, mypy, pytest)

### `pytest.ini`

Pytest configuration:
- Test paths
- File patterns
- Class patterns
- Function patterns
- Markers
- Options

### `.github/workflows/test.yml`

GitHub Actions CI/CD:
- Multi-version Python testing (3.8-3.12)
- Dependency caching
- Test execution
- Report generation
- Artifact upload
- Code coverage

### `.gitlab-ci.yml`

GitLab CI/CD:
- Pipeline stages
- Multi-version testing
- Artifact management
- Pages deployment

## 📦 Dependencies

### Core Dependencies
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-mock` - Mocking utilities
- `click` - CLI framework
- `pydantic` - Data validation
- `jinja2` - Template engine
- `rich` - Terminal UI
- `pyyaml` - YAML support
- `python-dotenv` - Environment variables

### LLM Support
- `openai` - OpenAI API
- `anthropic` - Anthropic API
- `litellm` - Multi-provider support

### Development Dependencies
- `black` - Code formatter
- `ruff` - Linter
- `mypy` - Type checker
- `pytest-cov` - Coverage

## 🎨 Design Patterns

### 1. Test Class Pattern

```python
class TestMyAgent(AgentTest):
    def setup(self):
        # Initialize
        pass
    
    @test_agent
    def test_something(self):
        # Test logic
        pass
    
    def teardown(self):
        # Cleanup
        pass
```

### 2. Decorator Pattern

```python
@test_agent  # Mark as test
@skip_test("reason")  # Skip test
@parametrize([...])  # Parametrize
def test_method(self):
    pass
```

### 3. Mock Pattern

```python
mock = MockLLM()
mock.add_response("prompt", "response")
mock.add_pattern(r"pattern", "response")
mock.add_function_response(matcher, "response")
```

### 4. Assertion Pattern

```python
self.assert_contains(output, "expected")
self.assert_latency(duration, max_seconds=1.0)
assert_no_pii(output)
```

### 5. Fixture Pattern

```python
@pytest.fixture
def my_fixture():
    return setup_data()

def test_with_fixture(my_fixture):
    assert my_fixture is not None
```

## 🔄 Workflow

### Development Workflow

```
1. Install → 2. Create Tests → 3. Run Tests → 4. Fix Issues → 5. Report
     ↓              ↓               ↓              ↓              ↓
pip install    write tests     praisonai-test   fix code    generate report
praisonai-test  in test_*.py        run                      --report html
```

### CI/CD Workflow

```
1. Push Code → 2. Run CI → 3. Execute Tests → 4. Generate Reports → 5. Deploy
      ↓             ↓             ↓                    ↓              ↓
  git push    GitHub Actions  praisonai-test run   Upload artifacts  Merge
                               --report junit
```

## 🎯 Use Cases

### 1. Unit Testing
Test individual agent functions in isolation using mocks.

### 2. Integration Testing
Test agent workflows end-to-end with real or mocked APIs.

### 3. Performance Testing
Track latency, cost, and token usage over time.

### 4. Safety Testing
Validate PII protection and hallucination prevention.

### 5. Regression Testing
Ensure changes don't break existing functionality.

### 6. CI/CD Integration
Automate testing in your deployment pipeline.

## 📊 Metrics

Framework provides:
- ✅ Test pass/fail counts
- ⏱️ Duration tracking
- 💰 Cost tracking
- 🎯 Token usage
- 📈 Coverage reports
- 📊 HTML dashboards

## 🔗 Integration Points

### Pytest
- Uses pytest as test runner
- Compatible with pytest plugins
- Supports pytest fixtures
- Works with pytest-cov

### CI/CD Systems
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Any system supporting JUnit XML

### LLM Providers
- OpenAI
- Anthropic
- Azure OpenAI
- LiteLLM (100+ providers)

## 📝 Best Practices

1. **Organize by Feature** - Group related tests
2. **Use Descriptive Names** - Clear test names
3. **Test One Thing** - Focused tests
4. **Mock by Default** - Use real APIs sparingly
5. **Track Coverage** - Aim for >80%
6. **Document Tests** - Add docstrings
7. **CI/CD Integration** - Automate testing

## 🚀 Future Enhancements

See `CHANGELOG.md` for planned features:
- Async test support
- Additional LLM providers
- Test parallelization
- Performance profiling
- VS Code extension
- Interactive test generation
- Test analytics dashboard

---

**Built with ❤️ for the AI agent development community**

