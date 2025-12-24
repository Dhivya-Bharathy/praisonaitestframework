"""
Command-line interface for PraisonAI Test
"""

import click
from pathlib import Path
from rich.console import Console

from praisonai_test.runner import TestRunner
from praisonai_test.reporter import TestReporter


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PraisonAI Test - Testing framework for AI agents"""
    pass


@cli.command()
@click.argument("name")
@click.option("--agent-type", default="basic", help="Agent type: basic, custom")
def new(name: str, agent_type: str):
    """Create a new test suite"""
    console.print(f"[bold]Creating new test suite: {name}[/bold]\n")
    
    # Create directory
    test_dir = Path(name)
    if test_dir.exists():
        console.print(f"[red]Directory already exists: {name}[/red]")
        return
    
    test_dir.mkdir(parents=True)
    
    # Create test file
    test_file = test_dir / "test_agent.py"
    test_template = _get_test_template(agent_type)
    test_file.write_text(test_template)
    
    # Create config file
    config_file = test_dir / "test_config.yaml"
    config_template = _get_config_template()
    config_file.write_text(config_template)
    
    # Create .env.example
    env_file = test_dir / ".env.example"
    env_template = _get_env_template()
    env_file.write_text(env_template)
    
    # Create conftest.py for pytest
    conftest_file = test_dir / "conftest.py"
    conftest_template = _get_conftest_template()
    conftest_file.write_text(conftest_template)
    
    # Create README
    readme_file = test_dir / "README.md"
    readme_template = _get_readme_template(name)
    readme_file.write_text(readme_template)
    
    console.print(f"[green]✅ Test suite created: {name}/[/green]")
    console.print("""
Next steps:
  1. cd {name}
  2. cp .env.example .env
  3. Edit .env with your configuration
  4. Run: praisonai-test run
""".format(name=name))


@cli.command()
@click.option("--path", default="tests", help="Path to test directory")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--report", default="console", help="Report format: console, json, html, junit")
@click.option("--output", "-o", help="Output file for report")
def run(path: str, verbose: bool, report: str, output: str):
    """Run agent tests"""
    console.print("[bold]Running PraisonAI Tests[/bold]\n")
    
    runner = TestRunner(verbose=verbose)
    runner.discover_tests(path)
    
    results = runner.run_all()
    
    # Generate report
    if report != "console" or output:
        reporter = TestReporter()
        reporter.generate_report(results, format=report, output=output)
    
    # Exit with error code if tests failed
    if results["summary"]["failed"] > 0:
        raise SystemExit(1)


@cli.command()
@click.argument("test_path")
@click.option("--report", default="console", help="Report format: console, json, html, junit")
@click.option("--output", "-o", help="Output file for report")
def run_file(test_path: str, report: str, output: str):
    """Run tests from a specific file"""
    runner = TestRunner(verbose=True)
    results = runner.run_file(test_path)
    
    # Generate report
    if report != "console" or output:
        reporter = TestReporter()
        reporter.generate_report(results, format=report, output=output)
    
    if results["summary"]["failed"] > 0:
        raise SystemExit(1)


@cli.command()
@click.option("--path", default="tests", help="Path to test directory")
@click.option("--format", default="html", help="Report format: console, json, html, junit")
@click.option("--output", "-o", required=True, help="Output file path")
def report(path: str, format: str, output: str):
    """Generate test report from previous run"""
    console.print("[bold]Generating test report[/bold]\n")
    
    runner = TestRunner(verbose=False)
    runner.discover_tests(path)
    results = runner.run_all()
    
    reporter = TestReporter()
    reporter.generate_report(results, format=format, output=output)


@cli.command()
def init():
    """Initialize testing in current directory"""
    console.print("[bold]Initializing PraisonAI Test[/bold]\n")
    
    # Create tests directory
    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    (tests_dir / "__init__.py").write_text("")
    
    # Create conftest.py
    conftest_file = tests_dir / "conftest.py"
    conftest_file.write_text(_get_conftest_template())
    
    # Create example test
    example_test = tests_dir / "test_example.py"
    example_test.write_text(_get_test_template("basic"))
    
    # Create pytest.ini
    pytest_ini = Path("pytest.ini")
    pytest_ini.write_text("""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
""")
    
    console.print("[green]✅ Initialized PraisonAI Test[/green]")
    console.print("""
Created:
  - tests/
  - tests/conftest.py
  - tests/test_example.py
  - pytest.ini

Run tests with: praisonai-test run
""")


@cli.command()
def version():
    """Show version information"""
    console.print("[bold]PraisonAI Test[/bold]")
    console.print("Version: 0.1.0")
    console.print("Homepage: https://praison.ai")


def _get_test_template(agent_type: str) -> str:
    """Get test template based on agent type"""
    return '''"""
AI Agent Tests
"""

from praisonai_test import AgentTest, test_agent


class TestMyAgent(AgentTest):
    """Test suite for my AI agent"""
    
    def setup(self):
        """Setup before each test"""
        # Initialize your agent here
        # self.agent = MyAgent()
        pass
    
    @test_agent
    def test_simple_query(self):
        """Test basic agent query"""
        # Example test
        result = "This is a mock response"
        
        # Use assertions
        self.assert_contains(result, "mock")
        self.assert_not_contains(result, "error")
    
    @test_agent
    def test_json_response(self):
        """Test JSON format response"""
        result = '{"status": "success", "data": "test"}'
        
        self.assert_json_valid(result)
        self.assert_contains(result, "success")
    
    @test_agent
    def test_performance(self):
        """Test agent response time"""
        import time
        
        start = time.time()
        # result = self.agent.run("test query")
        duration = time.time() - start
        
        self.assert_latency(duration, max_seconds=5.0)
'''


def _get_config_template() -> str:
    """Get config template"""
    return """# Test Configuration

agent:
  model: gpt-4
  temperature: 0.7
  max_tokens: 1000

test:
  timeout: 30
  retry_attempts: 3
  
mock:
  enabled: true
  responses:
    - prompt: "test"
      response: "mock response"
"""


def _get_env_template() -> str:
    """Get .env template"""
    return """# API Keys (for real agent testing)
# Leave empty to use mocks

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_KEY=

# Test Configuration
TEST_ENV=development
MOCK_ENABLED=true
"""


def _get_conftest_template() -> str:
    """Get conftest.py template"""
    return '''"""
Pytest configuration and fixtures
"""

import pytest
from praisonai_test import mock_llm


# Add your custom fixtures here

@pytest.fixture
def sample_agent():
    """Fixture for agent instance"""
    # Initialize your agent
    # return MyAgent()
    pass
'''


def _get_readme_template(name: str) -> str:
    """Get README template"""
    return f"""# {name} - AI Agent Tests

This test suite is created with PraisonAI Test framework.

## Setup

1. Install dependencies:
```bash
pip install praisonai-test
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running Tests

Run all tests:
```bash
praisonai-test run
```

Run with pytest:
```bash
pytest
```

Generate HTML report:
```bash
praisonai-test run --report html --output report.html
```

## Writing Tests

Create a test class:

```python
from praisonai_test import AgentTest, test_agent

class TestMyAgent(AgentTest):
    @test_agent
    def test_something(self):
        result = self.agent.run("test")
        self.assert_contains(result, "expected")
```

## Features

- ✅ Automated agent testing
- ✅ LLM mocking (no API calls needed)
- ✅ Rich assertions for AI outputs
- ✅ HTML/JSON/JUnit reports
- ✅ CI/CD integration

## Documentation

- Framework: https://github.com/MervinPraison/PraisonAI-Test
- Examples: https://github.com/MervinPraison/PraisonAI-Test/examples
"""


if __name__ == "__main__":
    cli()

