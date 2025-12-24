"""
Assertion helpers for AI agent testing
"""

import json
import re
from typing import Any, List, Optional, Union


def assert_agent_response(
    output: str,
    expected: str,
    mode: str = "contains",
    case_sensitive: bool = False
):
    """
    Assert agent response matches expectations
    
    Args:
        output: Agent output to validate
        expected: Expected string/pattern
        mode: "contains", "equals", "regex", "similarity"
        case_sensitive: Whether to match case
    """
    if not case_sensitive and mode != "regex":
        output = output.lower()
        expected = expected.lower()
    
    if mode == "contains":
        assert expected in output, (
            f"Expected '{expected}' not found in output.\n"
            f"Output: {output}"
        )
    elif mode == "equals":
        assert output == expected, (
            f"Output does not match expected.\n"
            f"Expected: {expected}\n"
            f"Actual: {output}"
        )
    elif mode == "regex":
        assert re.search(expected, output, re.IGNORECASE if not case_sensitive else 0), (
            f"Pattern '{expected}' not found in output.\n"
            f"Output: {output}"
        )
    elif mode == "similarity":
        score = _calculate_similarity(output, expected)
        assert score >= 0.8, (
            f"Similarity score {score:.2f} < 0.8\n"
            f"Output: {output}\n"
            f"Expected: {expected}"
        )
    else:
        raise ValueError(f"Unknown mode: {mode}")


def assert_contains(output: str, expected: str, case_sensitive: bool = False):
    """Assert that output contains expected string"""
    if not case_sensitive:
        output = output.lower()
        expected = expected.lower()
    
    assert expected in output, (
        f"Expected '{expected}' not found in output.\n"
        f"Output: {output}"
    )


def assert_not_contains(output: str, unexpected: str, case_sensitive: bool = False):
    """Assert that output does not contain unexpected string"""
    if not case_sensitive:
        output = output.lower()
        unexpected = unexpected.lower()
    
    assert unexpected not in output, (
        f"Unexpected '{unexpected}' found in output.\n"
        f"Output: {output}"
    )


def assert_json_valid(output: str, schema: Optional[dict] = None):
    """
    Assert that output is valid JSON
    
    Args:
        output: String to validate
        schema: Optional JSON schema to validate against
    """
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Output is not valid JSON: {str(e)}")
    
    if schema:
        # Simple schema validation
        _validate_schema(data, schema)


def assert_latency(duration: float, max_seconds: float):
    """Assert that operation completed within time limit"""
    assert duration <= max_seconds, (
        f"Operation took {duration:.2f}s, expected <= {max_seconds}s"
    )


def assert_cost(cost: float, max_cost: float, currency: str = "USD"):
    """Assert that operation cost is within budget"""
    assert cost <= max_cost, (
        f"Operation cost {currency} {cost:.4f}, expected <= {currency} {max_cost:.4f}"
    )


def assert_token_count(tokens: int, max_tokens: int):
    """Assert that token usage is within limit"""
    assert tokens <= max_tokens, (
        f"Token usage {tokens}, expected <= {max_tokens}"
    )


def assert_format(output: str, format_type: str):
    """
    Assert output format
    
    Supported formats: json, yaml, markdown, html, xml
    """
    if format_type == "json":
        try:
            json.loads(output)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Invalid JSON: {str(e)}")
    elif format_type == "yaml":
        try:
            import yaml
            yaml.safe_load(output)
        except Exception as e:
            raise AssertionError(f"Invalid YAML: {str(e)}")
    elif format_type == "markdown":
        # Basic markdown validation
        assert any(marker in output for marker in ["#", "**", "*", "-", "```"]), (
            "Output does not appear to be Markdown"
        )
    elif format_type == "html":
        assert "<" in output and ">" in output, "Output does not appear to be HTML"
    elif format_type == "xml":
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(output)
        except Exception as e:
            raise AssertionError(f"Invalid XML: {str(e)}")
    else:
        raise ValueError(f"Unknown format: {format_type}")


def assert_list_length(items: List, expected_length: int, mode: str = "exact"):
    """
    Assert list length
    
    Args:
        items: List to check
        expected_length: Expected length
        mode: "exact", "min", "max"
    """
    actual_length = len(items)
    
    if mode == "exact":
        assert actual_length == expected_length, (
            f"List length {actual_length}, expected {expected_length}"
        )
    elif mode == "min":
        assert actual_length >= expected_length, (
            f"List length {actual_length}, expected >= {expected_length}"
        )
    elif mode == "max":
        assert actual_length <= expected_length, (
            f"List length {actual_length}, expected <= {expected_length}"
        )
    else:
        raise ValueError(f"Unknown mode: {mode}")


def assert_all_items_match(items: List[str], pattern: str):
    """Assert all items in list match pattern"""
    for i, item in enumerate(items):
        assert re.search(pattern, item), (
            f"Item {i} does not match pattern '{pattern}': {item}"
        )


def assert_any_item_matches(items: List[str], pattern: str):
    """Assert at least one item in list matches pattern"""
    for item in items:
        if re.search(pattern, item):
            return
    
    raise AssertionError(
        f"No item matches pattern '{pattern}' in list: {items}"
    )


def assert_no_hallucination(output: str, source_docs: List[str], threshold: float = 0.7):
    """
    Assert output is grounded in source documents (simple version)
    
    Args:
        output: Agent output to validate
        source_docs: Source documents that should contain the information
        threshold: Minimum fraction of output that should be in sources
    """
    # Split output into sentences
    sentences = re.split(r'[.!?]+', output)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    grounded_count = 0
    for sentence in sentences:
        # Check if sentence words appear in source docs
        words = set(sentence.lower().split())
        for doc in source_docs:
            doc_words = set(doc.lower().split())
            overlap = len(words & doc_words)
            if overlap / len(words) > 0.5:  # 50% of words found
                grounded_count += 1
                break
    
    grounding_ratio = grounded_count / len(sentences) if sentences else 0
    
    assert grounding_ratio >= threshold, (
        f"Grounding ratio {grounding_ratio:.2f} < {threshold}\n"
        f"Output may contain hallucinations.\n"
        f"Output: {output}"
    )


def assert_no_pii(output: str):
    """Assert output does not contain PII (simple patterns)"""
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    }
    
    found_pii = []
    for pii_type, pattern in patterns.items():
        if re.search(pattern, output):
            found_pii.append(pii_type)
    
    assert not found_pii, (
        f"PII detected in output: {', '.join(found_pii)}\n"
        f"Output: {output}"
    )


def _calculate_similarity(str1: str, str2: str) -> float:
    """Calculate simple word-based similarity"""
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())
    
    if not words2:
        return 0.0
    
    overlap = len(words1 & words2)
    return overlap / len(words2)


def _validate_schema(data: Any, schema: dict):
    """Simple JSON schema validation"""
    if "type" in schema:
        expected_type = schema["type"]
        type_map = {
            "object": dict,
            "array": list,
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "null": type(None),
        }
        
        if expected_type in type_map:
            assert isinstance(data, type_map[expected_type]), (
                f"Expected type {expected_type}, got {type(data).__name__}"
            )
    
    if "properties" in schema and isinstance(data, dict):
        for key, value_schema in schema["properties"].items():
            if "required" in schema and key in schema["required"]:
                assert key in data, f"Required property '{key}' missing"
            
            if key in data:
                _validate_schema(data[key], value_schema)

