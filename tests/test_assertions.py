"""
Tests for assertion helpers
"""

import pytest
from praisonai_test.assertions import (
    assert_agent_response,
    assert_contains,
    assert_not_contains,
    assert_json_valid,
    assert_latency,
    assert_cost,
    assert_token_count,
    assert_format,
    assert_list_length,
    assert_all_items_match,
    assert_any_item_matches,
    assert_no_hallucination,
    assert_no_pii,
)


class TestBasicAssertions:
    """Test basic assertion functions"""
    
    def test_assert_contains(self):
        """Test assert_contains"""
        # Should pass
        assert_contains("hello world", "world")
        assert_contains("HELLO WORLD", "world", case_sensitive=False)
        
        # Should fail
        with pytest.raises(AssertionError):
            assert_contains("hello world", "missing")
    
    def test_assert_not_contains(self):
        """Test assert_not_contains"""
        # Should pass
        assert_not_contains("hello world", "missing")
        
        # Should fail
        with pytest.raises(AssertionError):
            assert_not_contains("hello world", "world")
    
    def test_assert_json_valid(self):
        """Test assert_json_valid"""
        # Valid JSON
        assert_json_valid('{"key": "value"}')
        assert_json_valid('["item1", "item2"]')
        assert_json_valid('123')
        assert_json_valid('"string"')
        
        # Invalid JSON
        with pytest.raises(AssertionError):
            assert_json_valid('not json')
        
        with pytest.raises(AssertionError):
            assert_json_valid('{invalid}')


class TestPerformanceAssertions:
    """Test performance-related assertions"""
    
    def test_assert_latency(self):
        """Test assert_latency"""
        # Should pass
        assert_latency(0.5, max_seconds=1.0)
        assert_latency(0.0, max_seconds=1.0)
        
        # Should fail
        with pytest.raises(AssertionError):
            assert_latency(2.0, max_seconds=1.0)
    
    def test_assert_cost(self):
        """Test assert_cost"""
        # Should pass
        assert_cost(0.05, max_cost=0.10)
        assert_cost(0.10, max_cost=0.10)
        
        # Should fail
        with pytest.raises(AssertionError):
            assert_cost(0.15, max_cost=0.10)
    
    def test_assert_token_count(self):
        """Test assert_token_count"""
        # Should pass
        assert_token_count(500, max_tokens=1000)
        assert_token_count(1000, max_tokens=1000)
        
        # Should fail
        with pytest.raises(AssertionError):
            assert_token_count(1500, max_tokens=1000)


class TestFormatAssertions:
    """Test format validation assertions"""
    
    def test_assert_format_json(self):
        """Test JSON format assertion"""
        assert_format('{"key": "value"}', "json")
        
        with pytest.raises(AssertionError):
            assert_format('not json', "json")
    
    def test_assert_format_markdown(self):
        """Test Markdown format assertion"""
        assert_format("# Heading\n\n**bold**", "markdown")
        assert_format("- list item", "markdown")
        
        with pytest.raises(AssertionError):
            assert_format("plain text", "markdown")
    
    def test_assert_format_html(self):
        """Test HTML format assertion"""
        assert_format("<div>content</div>", "html")
        assert_format("<p>paragraph</p>", "html")
        
        with pytest.raises(AssertionError):
            assert_format("plain text", "html")


class TestListAssertions:
    """Test list-related assertions"""
    
    def test_assert_list_length_exact(self):
        """Test exact list length assertion"""
        assert_list_length([1, 2, 3], 3, mode="exact")
        
        with pytest.raises(AssertionError):
            assert_list_length([1, 2], 3, mode="exact")
    
    def test_assert_list_length_min(self):
        """Test minimum list length assertion"""
        assert_list_length([1, 2, 3], 2, mode="min")
        assert_list_length([1, 2, 3], 3, mode="min")
        
        with pytest.raises(AssertionError):
            assert_list_length([1, 2], 3, mode="min")
    
    def test_assert_list_length_max(self):
        """Test maximum list length assertion"""
        assert_list_length([1, 2], 3, mode="max")
        assert_list_length([1, 2, 3], 3, mode="max")
        
        with pytest.raises(AssertionError):
            assert_list_length([1, 2, 3, 4], 3, mode="max")
    
    def test_assert_all_items_match(self):
        """Test all items match pattern"""
        assert_all_items_match(["test1", "test2", "test3"], r"test\d")
        
        with pytest.raises(AssertionError):
            assert_all_items_match(["test1", "fail", "test3"], r"test\d")
    
    def test_assert_any_item_matches(self):
        """Test any item matches pattern"""
        assert_any_item_matches(["fail1", "test2", "fail3"], r"test\d")
        
        with pytest.raises(AssertionError):
            assert_any_item_matches(["fail1", "fail2"], r"test\d")


class TestSafetyAssertions:
    """Test safety-related assertions"""
    
    def test_assert_no_pii_clean(self):
        """Test no PII detection with clean text"""
        assert_no_pii("This is clean text with no PII")
    
    def test_assert_no_pii_email(self):
        """Test PII detection for email"""
        with pytest.raises(AssertionError, match="email"):
            assert_no_pii("Contact me at user@example.com")
    
    def test_assert_no_pii_phone(self):
        """Test PII detection for phone"""
        with pytest.raises(AssertionError, match="phone"):
            assert_no_pii("Call me at 555-123-4567")
    
    def test_assert_no_pii_ssn(self):
        """Test PII detection for SSN"""
        with pytest.raises(AssertionError, match="ssn"):
            assert_no_pii("SSN is 123-45-6789")
    
    def test_assert_no_hallucination_grounded(self):
        """Test hallucination check with grounded output"""
        source_docs = [
            "PraisonAI is a testing framework",
            "It helps test AI agents",
        ]
        
        output = "PraisonAI is a testing framework that helps test AI agents"
        
        # Should pass - output is grounded in sources
        assert_no_hallucination(output, source_docs, threshold=0.3)
    
    def test_assert_no_hallucination_ungrounded(self):
        """Test hallucination check with ungrounded output"""
        source_docs = [
            "PraisonAI is a testing framework",
        ]
        
        output = "Completely unrelated content about something else entirely"
        
        # Should fail - output not grounded in sources
        with pytest.raises(AssertionError):
            assert_no_hallucination(output, source_docs, threshold=0.7)


class TestAgentResponseAssertion:
    """Test agent_response assertion"""
    
    def test_contains_mode(self):
        """Test contains mode"""
        assert_agent_response("hello world", "world", mode="contains")
        
        with pytest.raises(AssertionError):
            assert_agent_response("hello world", "missing", mode="contains")
    
    def test_equals_mode(self):
        """Test equals mode"""
        assert_agent_response("test", "test", mode="equals")
        
        with pytest.raises(AssertionError):
            assert_agent_response("test", "different", mode="equals")
    
    def test_regex_mode(self):
        """Test regex mode"""
        assert_agent_response("test123", r"test\d+", mode="regex")
        
        with pytest.raises(AssertionError):
            assert_agent_response("test", r"\d+", mode="regex")
    
    def test_similarity_mode(self):
        """Test similarity mode"""
        assert_agent_response(
            "The quick brown fox",
            "quick brown",
            mode="similarity"
        )
        
        with pytest.raises(AssertionError):
            assert_agent_response(
                "completely different",
                "nothing similar",
                mode="similarity"
            )
    
    def test_case_sensitivity(self):
        """Test case sensitivity option"""
        assert_agent_response("HELLO", "hello", mode="contains", case_sensitive=False)
        
        with pytest.raises(AssertionError):
            assert_agent_response("HELLO", "hello", mode="contains", case_sensitive=True)

