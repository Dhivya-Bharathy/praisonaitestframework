# 🔨 Create Test - Examples & Guide

Complete guide to using the "Create Test" feature in PraisonAI Test Streamlit UI.

## 🎯 Overview

The "Create Test" page helps you generate custom test code with:
- **6 pre-built templates** for common use cases
- **Interactive configuration** for all test parameters
- **Live test execution** to validate your test
- **One-click download** of generated code

## 📝 Available Templates

### 1. **Chatbot Testing**
Test conversational AI agents that respond to user messages.

**Example Use Case:**
- Testing greeting responses
- Validating conversation flow
- Checking response tone and content

**Generated Test:**
```python
class TestChatbot(AgentTest):
    def test_greeting_response(self):
        """Test chatbot responds to greetings"""
        result = self.mock.get_response("Hello! How are you?")
        self.assert_contains(result.content, "hello")
```

### 2. **Summarization Testing**
Test agents that summarize documents or long text.

**Example Use Case:**
- Testing summary quality
- Validating key points extraction
- Checking summary length

**Generated Test:**
```python
class TestSummarizer(AgentTest):
    def test_summary_quality(self):
        """Test that summary contains key points"""
        result = self.mock.get_response("Summarize: Long document...")
        self.assert_contains(result.content, "key_term")
```

### 3. **Code Generation Testing**
Test AI agents that generate code.

**Example Use Case:**
- Testing function generation
- Validating code syntax
- Checking for specific patterns

**Generated Test:**
```python
class TestCodeGen(AgentTest):
    def test_python_function(self):
        """Test generating a Python function"""
        result = self.mock.get_response("Write a Python function...")
        self.assert_contains(result.content, "def")
```

### 4. **Data Extraction Testing**
Test agents that extract structured data from text.

**Example Use Case:**
- Testing email extraction
- Validating phone number parsing
- Checking entity recognition

**Generated Test:**
```python
class TestDataExtractor(AgentTest):
    def test_extract_email(self):
        """Test extracting email from text"""
        result = self.mock.get_response("Extract email from: ...")
        self.assert_contains(result.content, "email@example.com")
```

### 5. **Q&A Agent Testing**
Test question-answering agents.

**Example Use Case:**
- Testing factual accuracy
- Validating source grounding
- Checking response relevance

**Generated Test:**
```python
class TestQAAgent(AgentTest):
    def test_factual_answer(self):
        """Test answering factual questions"""
        result = self.mock.get_response("What is the capital of France?")
        self.assert_contains(result.content, "Paris")
```

### 6. **Custom Testing**
Start from scratch with a blank template.

## ⚙️ Configuration Options

### Basic Configuration

| Field | Description | Example |
|-------|-------------|---------|
| **Test Class Name** | Name of the test class | `TestMyAgent` |
| **Test Description** | What the test suite does | `Test suite for my AI agent` |
| **Method Name** | Name of test method | `test_simple_query` |
| **Method Description** | What the test does | `Test basic agent query` |

### Input & Output

| Field | Description | Example |
|-------|-------------|---------|
| **Test Prompt** | Input to send to agent | `"What is 2+2?"` |
| **Mock Response** | Simulated agent response | `"The answer is 4"` |
| **Expected in Response** | Text that should appear | `"4"` |
| **Use Mock LLM** | Whether to use mocks | ✅ Recommended |

### Additional Assertions

#### 1. **Latency Check**
Ensures response time is within limits.

```python
self.assert_latency(duration, max_seconds=2.0)
```

**When to use:**
- Performance testing
- API timeout validation
- User experience requirements

#### 2. **Cost Check**
Validates API costs stay within budget.

```python
self.assert_cost(result.cost, max_cost=0.10)
```

**When to use:**
- Budget constraints
- Cost optimization testing
- Production cost monitoring

#### 3. **Token Check**
Ensures token usage is within limits.

```python
assert_token_count(result.tokens_used, max_tokens=1000)
```

**When to use:**
- Model context limits
- Token budget enforcement
- Prompt optimization

### Safety Checks

#### 1. **PII Detection**
Checks for personally identifiable information leakage.

```python
assert_no_pii(result.content)
```

**Detects:**
- Email addresses
- Phone numbers
- Social Security Numbers
- Credit card numbers

#### 2. **JSON Validation**
Ensures response is valid JSON.

```python
self.assert_json_valid(result.content)
```

**When to use:**
- API response validation
- Structured output requirements
- Data pipeline testing

## 🎮 Live Test Execution

After generating your test, click **"▶️ Run This Test Live"** to:

1. ✅ Execute the test in real-time
2. 📊 See results immediately
3. 🎈 Celebrate if it passes!
4. 🐛 Debug if it fails

**Example Output:**
```
✅ Test PASSED in 0.152s!

Status: ✅ PASSED
Duration: 0.152s
Test: test_simple_query
```

## 📥 Download & Use

### Step 1: Generate Test
Configure your test and click **"🚀 Generate Test Code"**

### Step 2: Download
Click **"💾 Download Test File"** to save as `.py` file

### Step 3: Run
Choose one of these methods:

**Option A: Using pytest**
```bash
pytest test_my_agent.py -v
```

**Option B: Using praisonai-test CLI**
```bash
praisonai-test run --path tests/
```

**Option C: Run directly**
```bash
python test_my_agent.py
```

## 💡 Best Practices

### 1. **Start with Templates**
Use pre-built templates as a starting point, then customize.

### 2. **Use Mocks by Default**
Enable "Use Mock LLM" to avoid API costs during development.

### 3. **Add Multiple Assertions**
Combine different assertion types for comprehensive testing:
```python
self.assert_contains(result, "expected")
self.assert_latency(duration, max_seconds=2.0)
self.assert_cost(cost, max_cost=0.05)
```

### 4. **Test Live Before Saving**
Always run the test live first to catch any issues.

### 5. **Add Safety Checks**
For production agents, enable PII detection and JSON validation.

## 🎯 Real-World Examples

### Example 1: Customer Support Bot

**Configuration:**
- Template: Chatbot
- Prompt: "I need help with my order"
- Expected: "help"
- Assertions: Latency (< 2s), PII detection

**Generated Test:**
```python
class TestSupportBot(AgentTest):
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "I need help with my order",
            mock_llm_response("I'd be happy to help you with your order!")
        )
    
    @test_agent
    def test_support_response(self):
        """Test support bot responds helpfully"""
        import time
        start = time.time()
        result = self.mock.get_response("I need help with my order")
        duration = time.time() - start
        
        self.assert_contains(result.content, "help")
        self.assert_latency(duration, max_seconds=2.0)
        assert_no_pii(result.content)
```

### Example 2: Document Analyzer

**Configuration:**
- Template: Data Extraction
- Prompt: "Extract key facts from this report"
- Expected: "fact"
- Assertions: JSON format, Token limit (< 500)

**Generated Test:**
```python
class TestDocAnalyzer(AgentTest):
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "Extract key facts from this report",
            mock_llm_response('{"facts": ["fact1", "fact2"]}', tokens_used=80)
        )
    
    @test_agent
    def test_fact_extraction(self):
        """Test extracting facts as JSON"""
        result = self.mock.get_response("Extract key facts from this report")
        
        self.assert_json_valid(result.content)
        self.assert_contains(result.content, "fact")
        assert_token_count(result.tokens_used, max_tokens=500)
```

### Example 3: Code Review Agent

**Configuration:**
- Template: Code Generator
- Prompt: "Review this code: def test(): pass"
- Expected: "function"
- Assertions: Latency (< 3s), Cost (< $0.05)

**Generated Test:**
```python
class TestCodeReviewer(AgentTest):
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "Review this code: def test(): pass",
            mock_llm_response("This function is empty and needs implementation", 
                            tokens_used=120, cost=0.012)
        )
    
    @test_agent
    def test_code_review(self):
        """Test code review suggestions"""
        import time
        start = time.time()
        result = self.mock.get_response("Review this code: def test(): pass")
        duration = time.time() - start
        
        self.assert_contains(result.content, "function")
        self.assert_latency(duration, max_seconds=3.0)
        self.assert_cost(result.cost, max_cost=0.05)
```

## 🔧 Troubleshooting

### Issue: Test fails immediately
**Solution:** Check that mock responses match the prompts exactly

### Issue: Import errors
**Solution:** Ensure all required imports are in the generated code

### Issue: Assertion fails
**Solution:** Adjust expected values or add case-insensitive matching

### Issue: Can't run live test
**Solution:** Make sure mock responses are configured correctly

## 📚 Further Reading

- [Main Documentation](README.md)
- [Getting Started Guide](GETTING_STARTED.md)
- [Assertion Reference](PROJECT_STRUCTURE.md)
- [Mocking Guide](examples/mock-llm-test/)

---

**Happy Testing! 🧪✨**

