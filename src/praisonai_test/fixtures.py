"""
Pytest fixtures for AI agent testing
"""

import pytest
from typing import Any, Callable, Dict
from praisonai_test.mocks import MockLLM, OpenAIMock, AnthropicMock, LiteLLMMock
from unittest.mock import patch


@pytest.fixture
def mock_llm():
    """Create a MockLLM instance for testing"""
    return MockLLM()


@pytest.fixture
def mock_openai(mock_llm):
    """Mock OpenAI client"""
    mock_client = OpenAIMock(mock_llm)
    with patch("openai.OpenAI", return_value=mock_client):
        yield mock_llm


@pytest.fixture
def mock_anthropic(mock_llm):
    """Mock Anthropic client"""
    mock_client = AnthropicMock(mock_llm)
    with patch("anthropic.Anthropic", return_value=mock_client):
        yield mock_llm


@pytest.fixture
def mock_litellm(mock_llm):
    """Mock LiteLLM"""
    mock_client = LiteLLMMock(mock_llm)
    with patch("litellm.completion", side_effect=mock_client.completion):
        yield mock_llm


def agent_fixture(setup_func: Callable = None):
    """
    Decorator to create agent fixtures
    
    Usage:
        @agent_fixture
        def my_agent():
            return MyAgent()
        
        # Or with setup
        @agent_fixture
        def my_agent_with_setup():
            agent = MyAgent()
            agent.load_config("test_config.yaml")
            return agent
    """
    def decorator(func: Callable):
        @pytest.fixture
        def fixture_wrapper(*args, **kwargs):
            if setup_func:
                setup_func()
            return func(*args, **kwargs)
        return fixture_wrapper
    
    if setup_func is None:
        # Used as @agent_fixture
        return decorator
    else:
        # Used as @agent_fixture()
        return decorator(setup_func)


@pytest.fixture
def temp_config(tmp_path):
    """Create temporary configuration directory"""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def mock_agent_config():
    """Provide default agent configuration"""
    return {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000,
        "timeout": 30,
    }


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables for each test"""
    # Clear API keys to prevent accidental real API calls
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_KEY", raising=False)


@pytest.fixture
def capture_agent_calls():
    """Capture all agent calls for analysis"""
    calls = []
    
    def capture(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            calls.append({
                "args": args,
                "kwargs": kwargs,
                "result": result,
            })
            return result
        return wrapper
    
    return capture, calls


@pytest.fixture
def mock_agent_response():
    """Fixture factory for creating mock agent responses"""
    def _create_response(
        content: str,
        model: str = "gpt-4",
        tokens: int = 100,
        cost: float = 0.01
    ):
        from praisonai_test.mocks import MockResponse
        return MockResponse(
            content=content,
            model=model,
            tokens_used=tokens,
            cost=cost
        )
    return _create_response


@pytest.fixture
def agent_test_context():
    """Provide testing context with common utilities"""
    return {
        "timestamp": None,
        "test_data": {},
        "mock_responses": [],
        "assertions": [],
    }

