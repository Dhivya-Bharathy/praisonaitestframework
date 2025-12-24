"""
Tests for AgentTest class
"""

import pytest
from praisonai_test import AgentTest, test_agent, skip_test, parametrize


class TestAgentTestClass:
    """Test AgentTest functionality"""
    
    def test_agent_test_creation(self):
        """Test AgentTest instance creation"""
        test = AgentTest()
        assert test is not None
        assert test.results == []
        assert test.agent is None
    
    def test_assert_contains(self):
        """Test assert_contains assertion"""
        test = AgentTest()
        
        # Should pass
        test.assert_contains("hello world", "world")
        test.assert_contains("HELLO WORLD", "world", case_sensitive=False)
        
        # Should fail
        with pytest.raises(AssertionError):
            test.assert_contains("hello world", "missing")
    
    def test_assert_not_contains(self):
        """Test assert_not_contains assertion"""
        test = AgentTest()
        
        # Should pass
        test.assert_not_contains("hello world", "missing")
        
        # Should fail
        with pytest.raises(AssertionError):
            test.assert_not_contains("hello world", "world")
    
    def test_assert_json_valid(self):
        """Test assert_json_valid assertion"""
        test = AgentTest()
        
        # Valid JSON
        test.assert_json_valid('{"key": "value"}')
        test.assert_json_valid('["item1", "item2"]')
        
        # Invalid JSON
        with pytest.raises(AssertionError):
            test.assert_json_valid('not json')
    
    def test_assert_latency(self):
        """Test assert_latency assertion"""
        test = AgentTest()
        
        # Should pass
        test.assert_latency(0.5, max_seconds=1.0)
        
        # Should fail
        with pytest.raises(AssertionError):
            test.assert_latency(2.0, max_seconds=1.0)
    
    def test_assert_cost(self):
        """Test assert_cost assertion"""
        test = AgentTest()
        
        # Should pass
        test.assert_cost(0.05, max_cost=0.10)
        
        # Should fail
        with pytest.raises(AssertionError):
            test.assert_cost(0.15, max_cost=0.10)
    
    def test_assert_equals(self):
        """Test assert_equals assertion"""
        test = AgentTest()
        
        # Should pass
        test.assert_equals(42, 42)
        test.assert_equals("test", "test")
        
        # Should fail
        with pytest.raises(AssertionError):
            test.assert_equals(42, 43)
    
    def test_assert_similarity(self):
        """Test assert_similarity assertion"""
        test = AgentTest()
        
        # Should pass
        test.assert_similarity(
            "The quick brown fox",
            "quick brown",
            min_score=0.5
        )
        
        # Should fail
        with pytest.raises(AssertionError):
            test.assert_similarity(
                "completely different",
                "nothing similar here",
                min_score=0.9
            )


class TestTestDecorators:
    """Test decorators"""
    
    def test_agent_decorator(self):
        """Test @test_agent decorator"""
        @test_agent
        def sample_test_method(self):
            pass
        
        assert hasattr(sample_test_method, '_is_agent_test')
        assert sample_test_method._is_agent_test is True
    
    def test_skip_decorator(self):
        """Test @skip_test decorator"""
        @skip_test("Not ready")
        @test_agent
        def sample_test(self):
            pass
        
        assert hasattr(sample_test, '_skip_test')
        assert sample_test._skip_test is True
        assert sample_test._skip_reason == "Not ready"
    
    def test_parametrize_decorator(self):
        """Test @parametrize decorator"""
        params = [{"a": 1}, {"a": 2}]
        
        @parametrize(params)
        @test_agent
        def sample_test(self, a):
            pass
        
        assert hasattr(sample_test, '_parametrize')
        assert sample_test._parametrize == params


class SampleAgentTest(AgentTest):
    """Sample test class for testing run_test"""
    
    def setup(self):
        self.setup_called = True
    
    def teardown(self):
        self.teardown_called = True
    
    @test_agent
    def test_passing(self):
        """A test that passes"""
        self.assert_equals(1, 1)
    
    @test_agent
    def test_failing(self):
        """A test that fails"""
        self.assert_equals(1, 2)


class TestRunTest:
    """Test running tests"""
    
    def test_run_passing_test(self):
        """Test running a passing test"""
        test_instance = SampleAgentTest()
        result = test_instance.run_test(lambda: test_instance.test_passing())
        
        assert result.status == "passed"
        assert result.test_name == "<lambda>"
        assert result.duration > 0
        assert result.error is None
    
    def test_run_failing_test(self):
        """Test running a failing test"""
        test_instance = SampleAgentTest()
        result = test_instance.run_test(lambda: test_instance.test_failing())
        
        assert result.status == "failed"
        assert result.test_name == "<lambda>"
        assert result.error is not None
    
    def test_setup_teardown_called(self):
        """Test that setup and teardown are called"""
        test_instance = SampleAgentTest()
        test_instance.setup_called = False
        test_instance.teardown_called = False
        
        test_instance.run_test(lambda: test_instance.test_passing())
        
        assert test_instance.setup_called is True
        assert test_instance.teardown_called is True


class TestTestResult:
    """Test TestResult dataclass"""
    
    def test_test_result_creation(self):
        """Test TestResult creation"""
        from praisonai_test.agent_test import TestResult
        
        result = TestResult(
            test_name="test_example",
            status="passed",
            duration=1.5,
            agent_output="output"
        )
        
        assert result.test_name == "test_example"
        assert result.status == "passed"
        assert result.duration == 1.5
        assert result.agent_output == "output"
    
    def test_test_result_to_dict(self):
        """Test TestResult to_dict method"""
        from praisonai_test.agent_test import TestResult
        
        result = TestResult(
            test_name="test_example",
            status="passed",
            duration=1.5,
            agent_output="output"
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict["test_name"] == "test_example"
        assert result_dict["status"] == "passed"
        assert "timestamp" in result_dict

