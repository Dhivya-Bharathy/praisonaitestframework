"""
Tests for mocking system
"""

import pytest
from praisonai_test.mocks import (
    MockLLM,
    MockResponse,
    mock_llm_response,
    OpenAIMock,
    AnthropicMock,
)


class TestMockResponse:
    """Test MockResponse dataclass"""
    
    def test_mock_response_creation(self):
        """Test creating MockResponse"""
        response = MockResponse(
            content="test response",
            model="gpt-4",
            tokens_used=50,
            cost=0.01
        )
        
        assert response.content == "test response"
        assert response.model == "gpt-4"
        assert response.tokens_used == 50
        assert response.cost == 0.01
    
    def test_mock_response_defaults(self):
        """Test MockResponse default values"""
        response = MockResponse(content="test")
        
        assert response.model == "gpt-4"
        assert response.tokens_used == 100
        assert response.cost == 0.01
    
    def test_mock_llm_response_helper(self):
        """Test mock_llm_response helper"""
        response = mock_llm_response(
            "test content",
            model="gpt-3.5",
            tokens_used=30
        )
        
        assert isinstance(response, MockResponse)
        assert response.content == "test content"
        assert response.model == "gpt-3.5"
        assert response.tokens_used == 30


class TestMockLLM:
    """Test MockLLM class"""
    
    def test_mock_llm_creation(self):
        """Test creating MockLLM instance"""
        mock = MockLLM()
        
        assert mock is not None
        assert mock.responses == []
        assert mock.call_history == []
    
    def test_add_exact_response(self):
        """Test adding exact match response"""
        mock = MockLLM()
        mock.add_response("test prompt", "test response")
        
        response = mock.get_response("test prompt")
        assert response.content == "test response"
    
    def test_add_pattern_response(self):
        """Test adding pattern-based response"""
        mock = MockLLM()
        mock.add_pattern(r".*capital.*", "It's a capital question")
        
        response = mock.get_response("What is the capital of France?")
        assert "capital question" in response.content
    
    def test_add_function_response(self):
        """Test adding function-based response"""
        mock = MockLLM()
        
        def is_math(prompt, **kwargs):
            return any(op in prompt for op in ['+', '-', '*', '/'])
        
        mock.add_function_response(is_math, "Math question detected")
        
        response = mock.get_response("What is 2+2?")
        assert "Math question" in response.content
    
    def test_default_response(self):
        """Test default response"""
        mock = MockLLM()
        mock.set_default_response("Default response")
        
        response = mock.get_response("unmatched prompt")
        assert response.content == "Default response"
    
    def test_call_tracking(self):
        """Test call history tracking"""
        mock = MockLLM()
        mock.add_response("test", "response")
        
        mock.get_response("test")
        mock.get_response("test")
        
        assert mock.get_call_count() == 2
    
    def test_last_call(self):
        """Test getting last call"""
        mock = MockLLM()
        mock.add_response("first", "response1")
        mock.add_response("second", "response2")
        
        mock.get_response("first")
        mock.get_response("second", extra_param="value")
        
        last_call = mock.get_last_call()
        assert last_call["prompt"] == "second"
        assert last_call["kwargs"]["extra_param"] == "value"
    
    def test_reset_history(self):
        """Test resetting call history"""
        mock = MockLLM()
        mock.add_response("test", "response")
        
        mock.get_response("test")
        assert mock.get_call_count() == 1
        
        mock.reset()
        assert mock.get_call_count() == 0


class TestOpenAIMock:
    """Test OpenAI mocking"""
    
    def test_openai_mock_creation(self):
        """Test creating OpenAI mock"""
        mock_llm = MockLLM()
        openai_mock = OpenAIMock(mock_llm)
        
        assert openai_mock is not None
        assert hasattr(openai_mock, 'chat')
    
    def test_openai_chat_completion(self):
        """Test OpenAI chat completion mock"""
        mock_llm = MockLLM()
        mock_llm.add_response("Hello", "Hi there!")
        
        openai_mock = OpenAIMock(mock_llm)
        
        response = openai_mock.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        assert response.choices[0].message.content == "Hi there!"
        assert hasattr(response, 'usage')


class TestAnthropicMock:
    """Test Anthropic mocking"""
    
    def test_anthropic_mock_creation(self):
        """Test creating Anthropic mock"""
        mock_llm = MockLLM()
        anthropic_mock = AnthropicMock(mock_llm)
        
        assert anthropic_mock is not None
        assert hasattr(anthropic_mock, 'messages')
    
    def test_anthropic_message_creation(self):
        """Test Anthropic message creation mock"""
        mock_llm = MockLLM()
        mock_llm.add_response("Hello", "Hi there!")
        
        anthropic_mock = AnthropicMock(mock_llm)
        
        response = anthropic_mock.messages.create(
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        assert response.content[0].text == "Hi there!"
        assert hasattr(response, 'usage')


class TestMockIntegration:
    """Test mock integration scenarios"""
    
    def test_multiple_providers(self):
        """Test using multiple provider mocks"""
        mock_llm = MockLLM()
        mock_llm.add_response("test", "response")
        
        openai_mock = OpenAIMock(mock_llm)
        anthropic_mock = AnthropicMock(mock_llm)
        
        # Both should work with same mock_llm
        openai_response = openai_mock.chat.completions.create(
            messages=[{"role": "user", "content": "test"}]
        )
        anthropic_response = anthropic_mock.messages.create(
            messages=[{"role": "user", "content": "test"}]
        )
        
        assert "response" in openai_response.choices[0].message.content
        assert "response" in anthropic_response.content[0].text
        
        # Both calls should be tracked
        assert mock_llm.get_call_count() == 2
    
    def test_mock_with_metadata(self):
        """Test mock response with metadata"""
        mock_llm = MockLLM()
        
        response = mock_llm_response(
            "test content",
            model="gpt-4",
            tokens_used=50,
            cost=0.02,
            latency=0.5,
            metadata={"source": "mock"}
        )
        
        mock_llm.add_response("test", response)
        
        result = mock_llm.get_response("test")
        assert result.metadata["source"] == "mock"
        assert result.latency == 0.5

