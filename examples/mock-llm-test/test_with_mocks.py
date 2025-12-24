"""
Example: Testing AI Agents with LLM Mocking
"""

import pytest
from praisonai_test import AgentTest, test_agent, MockLLM, mock_llm_response


class TestWithMockLLM(AgentTest):
    """Example of testing with mocked LLM responses"""
    
    def setup(self):
        """Setup mock LLM"""
        self.mock = MockLLM()
        
        # Add predefined responses
        self.mock.add_response(
            "What is 2+2?",
            mock_llm_response("The answer is 4", tokens_used=20, cost=0.001)
        )
        
        self.mock.add_response(
            "Write a haiku about testing",
            mock_llm_response(
                "Tests run with grace\nMocks replace the real API\nCode flows bug-free now",
                tokens_used=50,
                cost=0.002
            )
        )
        
        # Add pattern-based response
        self.mock.add_pattern(
            r".*capital.*",
            mock_llm_response("I can help with geography questions")
        )
    
    @test_agent
    def test_with_exact_mock(self):
        """Test with exact prompt matching"""
        response = self.mock.get_response("What is 2+2?")
        
        assert response.content == "The answer is 4"
        assert response.tokens_used == 20
        self.assert_contains(response.content, "4")
    
    @test_agent
    def test_with_pattern_mock(self):
        """Test with pattern matching"""
        response = self.mock.get_response("What is the capital of France?")
        
        self.assert_contains(response.content, "geography")
    
    @test_agent
    def test_with_function_matcher(self):
        """Test with function-based matching"""
        def is_math_question(prompt, **kwargs):
            return any(op in prompt for op in ['+', '-', '*', '/'])
        
        self.mock.add_function_response(
            is_math_question,
            mock_llm_response("This is a math question")
        )
        
        response = self.mock.get_response("What is 10 * 5?")
        self.assert_contains(response.content, "math")
    
    @test_agent
    def test_default_response(self):
        """Test default response for unmatched prompts"""
        self.mock.set_default_response("I don't know")
        
        response = self.mock.get_response("Random question")
        self.assert_contains(response.content, "don't know")
    
    @test_agent
    def test_call_tracking(self):
        """Test that calls are tracked"""
        self.mock.get_response("What is 2+2?")
        self.mock.get_response("Write a haiku about testing")
        
        assert self.mock.get_call_count() == 2
        
        last_call = self.mock.get_last_call()
        assert "haiku" in last_call["prompt"]


@pytest.fixture
def mock_openai_client(mock_openai):
    """Fixture for mocked OpenAI client"""
    # Setup responses
    mock_openai.add_response(
        "Hello, AI!",
        mock_llm_response("Hello! How can I help you today?")
    )
    return mock_openai


class TestWithOpenAIMock(AgentTest):
    """Example of testing with OpenAI mock"""
    
    @test_agent
    def test_openai_chat(self, mock_openai_client):
        """Test with mocked OpenAI"""
        # This would normally call OpenAI API
        # But it's mocked, so no real API call is made
        
        # Simulate OpenAI-like usage
        mock_openai_client.add_response(
            "What is AI?",
            mock_llm_response("AI stands for Artificial Intelligence")
        )
        
        response = mock_openai_client.get_response("What is AI?")
        self.assert_contains(response.content, "Artificial Intelligence")


class TestAgentWithMockIntegration(AgentTest):
    """Example of real agent integration with mocks"""
    
    def setup(self):
        """Setup agent with mocked LLM"""
        self.mock = MockLLM()
        self.setup_mock(self.mock)
        
        # Configure mock responses for agent
        self.mock.add_pattern(
            r".*summarize.*",
            mock_llm_response(
                "Summary: This is a test document about AI testing.",
                tokens_used=30
            )
        )
        
        self.mock.add_pattern(
            r".*analyze.*",
            mock_llm_response(
                "Analysis: The document discusses testing methodologies.",
                tokens_used=40
            )
        )
    
    @test_agent
    def test_agent_summarization(self):
        """Test agent summarization with mock"""
        result = self.mock.get_response(
            "Please summarize this document about AI testing"
        )
        
        self.assert_contains(result.content, "Summary")
        self.assert_contains(result.content, "test")
        
        # Verify mock was called
        assert self.mock.get_call_count() >= 1
    
    @test_agent
    def test_agent_analysis(self):
        """Test agent analysis with mock"""
        result = self.mock.get_response(
            "Please analyze this document"
        )
        
        self.assert_contains(result.content, "Analysis")
        
    @test_agent
    def test_agent_token_usage(self):
        """Test agent token tracking with mock"""
        result = self.mock.get_response("Please summarize this document")
        
        # Check token usage from mock
        from praisonai_test.assertions import assert_token_count
        assert_token_count(result.tokens_used, max_tokens=100)
    
    @test_agent
    def test_multiple_calls(self):
        """Test agent with multiple calls"""
        # Reset call history
        self.mock.reset()
        
        # Make multiple calls
        self.mock.get_response("Please summarize")
        self.mock.get_response("Please analyze")
        
        # Verify all calls were tracked
        assert self.mock.get_call_count() == 2


# Example: Pytest integration with fixtures
def test_with_pytest_fixtures(mock_llm):
    """Example using pytest fixtures"""
    # Setup mock
    mock_llm.add_response("test", "response")
    
    # Use mock
    result = mock_llm.get_response("test")
    
    assert result.content == "response"

