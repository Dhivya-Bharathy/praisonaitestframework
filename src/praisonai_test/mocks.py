"""
LLM mocking system for testing AI agents without real API calls
"""

from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass
from unittest.mock import Mock, patch
import json


@dataclass
class MockResponse:
    """Mock LLM response"""
    
    content: str
    model: str = "gpt-4"
    tokens_used: int = 100
    cost: float = 0.01
    latency: float = 0.5
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MockLLM:
    """
    Mock LLM for testing without real API calls
    
    Usage:
        mock = MockLLM()
        mock.add_response("What is 2+2?", "The answer is 4")
        
        # Or with pattern matching
        mock.add_pattern(r".*math.*", "I can help with math")
    """
    
    def __init__(self):
        self.responses: List[tuple] = []  # (pattern/exact, response, is_pattern)
        self.call_history: List[Dict[str, Any]] = []
        self.default_response = "Mock response"
        
    def add_response(self, prompt: str, response: Union[str, MockResponse]):
        """Add exact match response"""
        if isinstance(response, str):
            response = MockResponse(content=response)
        self.responses.append((prompt, response, False))
        
    def add_pattern(self, pattern: str, response: Union[str, MockResponse]):
        """Add pattern-based response"""
        import re
        if isinstance(response, str):
            response = MockResponse(content=response)
        self.responses.append((re.compile(pattern), response, True))
        
    def add_function_response(self, matcher: Callable, response: Union[str, MockResponse]):
        """Add function-based response matching"""
        if isinstance(response, str):
            response = MockResponse(content=response)
        self.responses.append((matcher, response, "function"))
        
    def set_default_response(self, response: Union[str, MockResponse]):
        """Set default response for unmatched prompts"""
        if isinstance(response, str):
            response = MockResponse(content=response)
        self.default_response = response
        
    def get_response(self, prompt: str, **kwargs) -> MockResponse:
        """Get mock response for prompt"""
        self.call_history.append({
            "prompt": prompt,
            "kwargs": kwargs,
        })
        
        # Try to find matching response
        for matcher, response, match_type in self.responses:
            if match_type == False:  # Exact match
                if prompt == matcher:
                    return response
            elif match_type == True:  # Pattern match
                if matcher.match(prompt):
                    return response
            elif match_type == "function":  # Function match
                if matcher(prompt, **kwargs):
                    return response
        
        # Return default response
        if isinstance(self.default_response, str):
            return MockResponse(content=self.default_response)
        return self.default_response
    
    def get_call_count(self) -> int:
        """Get number of calls made"""
        return len(self.call_history)
    
    def get_last_call(self) -> Optional[Dict[str, Any]]:
        """Get last call details"""
        return self.call_history[-1] if self.call_history else None
    
    def reset(self):
        """Reset call history"""
        self.call_history = []


def mock_llm_response(content: str, **kwargs) -> MockResponse:
    """
    Helper to create a mock response
    
    Usage:
        response = mock_llm_response("Hello", model="gpt-4", tokens_used=50)
    """
    return MockResponse(content=content, **kwargs)


class OpenAIMock:
    """Mock for OpenAI API"""
    
    def __init__(self, mock_llm: MockLLM):
        self.mock_llm = mock_llm
        self.chat = self.Chat(mock_llm)
        
    class Chat:
        def __init__(self, mock_llm: MockLLM):
            self.mock_llm = mock_llm
            self.completions = self.Completions(mock_llm)
            
        class Completions:
            def __init__(self, mock_llm: MockLLM):
                self.mock_llm = mock_llm
                
            def create(self, messages: List[Dict], **kwargs):
                """Mock chat completion"""
                # Extract last user message
                user_message = ""
                for msg in reversed(messages):
                    if msg.get("role") == "user":
                        user_message = msg.get("content", "")
                        break
                
                response = self.mock_llm.get_response(user_message, **kwargs)
                
                # Return OpenAI-like response object
                return type('MockChatCompletion', (), {
                    'choices': [
                        type('Choice', (), {
                            'message': type('Message', (), {
                                'content': response.content,
                                'role': 'assistant'
                            })(),
                            'finish_reason': 'stop'
                        })()
                    ],
                    'model': response.model,
                    'usage': type('Usage', (), {
                        'total_tokens': response.tokens_used,
                        'prompt_tokens': response.tokens_used // 2,
                        'completion_tokens': response.tokens_used // 2,
                    })()
                })()


class AnthropicMock:
    """Mock for Anthropic API"""
    
    def __init__(self, mock_llm: MockLLM):
        self.mock_llm = mock_llm
        self.messages = self.Messages(mock_llm)
        
    class Messages:
        def __init__(self, mock_llm: MockLLM):
            self.mock_llm = mock_llm
            
        def create(self, messages: List[Dict], **kwargs):
            """Mock message creation"""
            # Extract last user message
            user_message = ""
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        user_message = " ".join([c.get("text", "") for c in content])
                    else:
                        user_message = content
                    break
            
            response = self.mock_llm.get_response(user_message, **kwargs)
            
            # Return Anthropic-like response object
            return type('MockMessage', (), {
                'content': [type('ContentBlock', (), {
                    'text': response.content
                })()],
                'model': response.model,
                'usage': type('Usage', (), {
                    'input_tokens': response.tokens_used // 2,
                    'output_tokens': response.tokens_used // 2,
                })()
            })()


class LiteLLMMock:
    """Mock for LiteLLM"""
    
    def __init__(self, mock_llm: MockLLM):
        self.mock_llm = mock_llm
        
    def completion(self, messages: List[Dict], **kwargs):
        """Mock completion"""
        # Extract last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        response = self.mock_llm.get_response(user_message, **kwargs)
        
        # Return LiteLLM-like response
        return type('MockCompletion', (), {
            'choices': [
                type('Choice', (), {
                    'message': type('Message', (), {
                        'content': response.content,
                        'role': 'assistant'
                    })()
                })()
            ],
            'model': response.model,
            'usage': {
                'total_tokens': response.tokens_used,
                'prompt_tokens': response.tokens_used // 2,
                'completion_tokens': response.tokens_used // 2,
            }
        })()


def create_mock_llm_patch(mock_llm: MockLLM, provider: str = "openai"):
    """
    Create a patch context for LLM provider
    
    Usage:
        mock = MockLLM()
        mock.add_response("test", "response")
        
        with create_mock_llm_patch(mock, "openai"):
            # OpenAI calls will use mock
            client = OpenAI()
            response = client.chat.completions.create(...)
    """
    if provider == "openai":
        mock_client = OpenAIMock(mock_llm)
        return patch("openai.OpenAI", return_value=mock_client)
    elif provider == "anthropic":
        mock_client = AnthropicMock(mock_llm)
        return patch("anthropic.Anthropic", return_value=mock_client)
    elif provider == "litellm":
        mock_client = LiteLLMMock(mock_llm)
        return patch("litellm.completion", side_effect=mock_client.completion)
    else:
        raise ValueError(f"Unknown provider: {provider}")

