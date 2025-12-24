"""
PraisonAI Test - Testing framework for AI agents
"""

from praisonai_test.agent_test import AgentTest, test_agent, skip_test, parametrize
from praisonai_test.assertions import (
    assert_agent_response,
    assert_contains,
    assert_not_contains,
    assert_json_valid,
    assert_latency,
    assert_cost,
)
from praisonai_test.mocks import MockLLM, mock_llm_response
from praisonai_test.fixtures import agent_fixture, mock_openai, mock_anthropic
from praisonai_test.runner import TestRunner
from praisonai_test.reporter import TestReporter

__version__ = "1.0.0"

__all__ = [
    # Core classes
    "AgentTest",
    "TestRunner",
    "TestReporter",
    # Decorators
    "test_agent",
    "skip_test",
    "parametrize",
    "agent_fixture",
    # Assertions
    "assert_agent_response",
    "assert_contains",
    "assert_not_contains",
    "assert_json_valid",
    "assert_latency",
    "assert_cost",
    # Mocking
    "MockLLM",
    "mock_llm_response",
    "mock_openai",
    "mock_anthropic",
]

