"""
Core AgentTest class for defining and running AI agent tests
"""

import time
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class TestResult:
    """Result of a single agent test"""
    
    test_name: str
    status: str  # "passed", "failed", "skipped"
    duration: float
    agent_output: Any
    expected_output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "test_name": self.test_name,
            "status": self.status,
            "duration": self.duration,
            "agent_output": str(self.agent_output),
            "expected_output": str(self.expected_output) if self.expected_output else None,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class AgentTest:
    """
    Base class for defining AI agent tests
    
    Usage:
        class MyAgentTest(AgentTest):
            @test_agent
            def test_simple_query(self):
                result = self.agent.run("What is 2+2?")
                self.assert_contains(result, "4")
    """
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.agent = None
        self.mock_llm = None
        self.config: Dict[str, Any] = {}
        
    def setup(self):
        """Override this method for test setup"""
        pass
    
    def teardown(self):
        """Override this method for test cleanup"""
        pass
    
    def setup_agent(self, agent: Any):
        """Set the agent to test"""
        self.agent = agent
        
    def setup_mock(self, mock_llm: Any):
        """Set up LLM mocking"""
        self.mock_llm = mock_llm
        
    def run_test(self, test_func: Callable) -> TestResult:
        """Run a single test function"""
        test_name = test_func.__name__
        start_time = time.time()
        
        try:
            self.setup()
            result = test_func(self)
            duration = time.time() - start_time
            
            test_result = TestResult(
                test_name=test_name,
                status="passed",
                duration=duration,
                agent_output=result,
                metadata={
                    "test_doc": test_func.__doc__ or "",
                }
            )
        except AssertionError as e:
            duration = time.time() - start_time
            test_result = TestResult(
                test_name=test_name,
                status="failed",
                duration=duration,
                agent_output=None,
                error=str(e),
            )
        except Exception as e:
            duration = time.time() - start_time
            test_result = TestResult(
                test_name=test_name,
                status="failed",
                duration=duration,
                agent_output=None,
                error=f"Unexpected error: {str(e)}",
            )
        finally:
            self.teardown()
            
        self.results.append(test_result)
        return test_result
    
    def assert_contains(self, output: str, expected: str, case_sensitive: bool = False):
        """Assert that output contains expected string"""
        if not case_sensitive:
            output = output.lower()
            expected = expected.lower()
        
        assert expected in output, (
            f"Expected '{expected}' not found in output.\n"
            f"Output: {output}"
        )
    
    def assert_not_contains(self, output: str, unexpected: str, case_sensitive: bool = False):
        """Assert that output does not contain unexpected string"""
        if not case_sensitive:
            output = output.lower()
            unexpected = unexpected.lower()
        
        assert unexpected not in output, (
            f"Unexpected '{unexpected}' found in output.\n"
            f"Output: {output}"
        )
    
    def assert_json_valid(self, output: str):
        """Assert that output is valid JSON"""
        try:
            json.loads(output)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Output is not valid JSON: {str(e)}")
    
    def assert_latency(self, duration: float, max_seconds: float):
        """Assert that operation completed within time limit"""
        assert duration <= max_seconds, (
            f"Operation took {duration:.2f}s, expected <= {max_seconds}s"
        )
    
    def assert_cost(self, cost: float, max_cost: float):
        """Assert that operation cost is within budget"""
        assert cost <= max_cost, (
            f"Operation cost ${cost:.4f}, expected <= ${max_cost:.4f}"
        )
    
    def assert_equals(self, actual: Any, expected: Any):
        """Assert equality"""
        assert actual == expected, (
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )
    
    def assert_similarity(self, output: str, expected: str, min_score: float = 0.8):
        """Assert semantic similarity between outputs"""
        # Simple word overlap for now, can be enhanced with embeddings
        output_words = set(output.lower().split())
        expected_words = set(expected.lower().split())
        
        if not expected_words:
            return
        
        overlap = len(output_words & expected_words)
        score = overlap / len(expected_words)
        
        assert score >= min_score, (
            f"Similarity score {score:.2f} < {min_score}\n"
            f"Output: {output}\n"
            f"Expected: {expected}"
        )


def test_agent(func: Callable) -> Callable:
    """
    Decorator to mark a method as an agent test
    
    Usage:
        @test_agent
        def test_my_agent(self):
            result = self.agent.run("test")
            self.assert_contains(result, "expected")
    """
    func._is_agent_test = True
    return func


def skip_test(reason: str = ""):
    """
    Decorator to skip a test
    
    Usage:
        @skip_test("Not implemented yet")
        @test_agent
        def test_future_feature(self):
            pass
    """
    def decorator(func: Callable) -> Callable:
        func._skip_test = True
        func._skip_reason = reason
        return func
    return decorator


def parametrize(params: List[Dict[str, Any]]):
    """
    Decorator to run test with multiple parameters
    
    Usage:
        @parametrize([
            {"input": "2+2", "expected": "4"},
            {"input": "3+3", "expected": "6"},
        ])
        @test_agent
        def test_math(self, input, expected):
            result = self.agent.run(input)
            self.assert_contains(result, expected)
    """
    def decorator(func: Callable) -> Callable:
        func._parametrize = params
        return func
    return decorator

