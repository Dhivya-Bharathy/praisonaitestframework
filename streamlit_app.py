"""
PraisonAI Test - Streamlit UI
Interactive interface for testing AI agents
"""

import streamlit as st
import sys
import time
from pathlib import Path
import json
from datetime import datetime
import traceback
from openai import OpenAI

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from praisonai_test import (
    AgentTest,
    test_agent,
    MockLLM,
    mock_llm_response,
    TestRunner,
    TestReporter,
)
from praisonai_test.assertions import (
    assert_contains,
    assert_json_valid,
    assert_latency,
    assert_cost,
    assert_no_pii,
    assert_token_count,
)

# OpenAI API Configuration
# Get API key from session state (user input), Streamlit secrets, or environment variable
import os
OPENAI_API_KEY = st.session_state.get('user_api_key', st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")))
OPENAI_MODEL = "gpt-4o-mini"

# Page configuration
st.set_page_config(
    page_title="PraisonAI Test Framework",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧪 PraisonAI Test Framework</h1>', unsafe_allow_html=True)
st.markdown("### Testing Framework for AI Agents with Mocking & CI/CD Integration")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=PraisonAI+Test", use_container_width=True)
    
    st.markdown("## 🎯 Navigation")
    page = st.radio(
        "Choose a section:",
        ["Overview", "Live Demo", "Example Tests", "Create Test", "Documentation"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("- [GitHub](https://github.com/MervinPraison/PraisonAI-Test)")
    st.markdown("- [Documentation](https://praison.ai)")
    st.markdown("- [Examples](https://github.com/MervinPraison/PraisonAI-Test/examples)")
    
    st.markdown("---")
    st.markdown("### ⚙️ API Settings")
    
    # Check if API key is configured
    has_api_key = bool(OPENAI_API_KEY)
    
    if has_api_key:
        st.success("✅ API Key: Configured")
    else:
        st.error("❌ API Key: Not Set")
    
    with st.expander("🔑 Configure OpenAI API Key", expanded=not has_api_key):
        st.markdown("**Current Model:** gpt-4o-mini")
        st.markdown("**Status:** " + ("✅ Active" if has_api_key else "❌ Not configured"))
        
        custom_key = st.text_input(
            "Enter your OpenAI API key:",
            value="",
            type="password",
            placeholder="sk-proj-...",
            help="Get your key at: https://platform.openai.com/api-keys"
        )
        
        if custom_key:
            # Update the global API key for this session
            st.session_state['user_api_key'] = custom_key
            st.success("✅ API key set for this session!")
            st.info("🔄 Refresh the page to use the new key")
        
        st.markdown("---")
        st.markdown("💡 **How to Add API Key:**")
        st.markdown("**Option 1: In Streamlit Cloud (Recommended)**")
        st.markdown("1. Click 'Manage app' → Settings → Secrets")
        st.markdown("2. Add: `OPENAI_API_KEY = \"your-key\"`")
        st.markdown("")
        st.markdown("**Option 2: Enter above (temporary)**")
        st.markdown("Only works for current session")
        st.markdown("")
        st.markdown("💰 **Get Credits:** [OpenAI Billing](https://platform.openai.com/settings/organization/billing/overview)")
        st.markdown("$5 = ~50,000 tests!")
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Version", "0.1.0")
    st.metric("Python", "3.8+")
    st.metric("Tests Run", st.session_state.get('tests_run', 0))

# Main content based on page selection
if page == "Overview":
    st.markdown("## 🚀 What is PraisonAI Test?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>✅ Easy Testing</h3>
            <p>Decorator-based testing similar to pytest but designed for AI agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎭 Smart Testing</h3>
            <p>FREE Mock mode by default. Optional REAL ChatGPT testing when needed!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Rich Reports</h3>
            <p>Beautiful HTML, JSON, JUnit reports with detailed insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Core Capabilities
        - ✅ **Simple Test Syntax** - Decorator-based like pytest
        - ✅ **FREE Mock Testing** - No API costs (default mode)
        - ✅ **Optional Real AI** - Use ChatGPT when needed
        - ✅ **Rich Assertions** - AI-specific validations
        - ✅ **Performance Testing** - Latency & cost tracking
        - ✅ **Safety Validation** - PII & hallucination checks
        """)
    
    with col2:
        st.markdown("""
        ### Developer Experience
        - 🚀 **CLI Tools** - Create, run, report
        - 📊 **Multiple Formats** - Console, JSON, HTML, JUnit
        - 🔄 **CI/CD Ready** - GitHub Actions, GitLab CI
        - 🎨 **Beautiful Output** - Rich terminal UI
        - 🔌 **Provider Support** - OpenAI, Anthropic, LiteLLM
        """)
    
    st.markdown("## 🎯 Complete Development Cycle")
    
    st.markdown("""
    ```
    Build → Test → Deploy → Measure
      ↓       ↓       ↓        ↓
    PraisonAI → PraisonAI-Test → PraisonAI-SVC → PraisonAIBench
               (THIS FRAMEWORK!)
    ```
    """)
    
    st.markdown("## 📦 Quick Install")
    
    st.code("pip install praisonai-test", language="bash")
    
    st.markdown("## 🎬 Quick Start")
    
    st.code("""# Create new test suite
praisonai-test new my-tests

# Run tests
praisonai-test run

# Generate HTML report
praisonai-test run --report html --output report.html""", language="bash")

elif page == "Live Demo":
    st.markdown("## 🎬 Live Demo - Interactive Testing!")
    
    # Prominent API key notice
    st.warning("""
    ⚠️ **OpenAI API Key Required for Real ChatGPT Testing**
    
    To use REAL ChatGPT API (optional feature), you need to add your OpenAI API key:
    
    1. **On Streamlit Cloud:** Click "⚙️ API Settings" in the sidebar, then add your key
    2. **Locally:** Create `.streamlit/secrets.toml` file with your key
    3. **Get API Key:** https://platform.openai.com/api-keys
    
    💡 **No API key? No problem!** The framework works perfectly in **FREE Mock Mode** (no API key needed)
    """)
    
    # Option to switch between mock and real
    use_real_api = st.checkbox("🤖 Use REAL ChatGPT API (requires credits)", value=False, 
                                help="Check this to use real OpenAI API. Leave unchecked for free mock testing.")
    
    if use_real_api:
        st.info("⚡ Using REAL ChatGPT (gpt-4o-mini) - costs ~$0.00001 per test")
    else:
        st.success("🎭 Using FREE Mock Mode - No API calls, instant results!")
    
    st.markdown("### Run Example Tests")
    
    button_text = "▶️ Run Sample Tests" + (" with REAL ChatGPT 🤖" if use_real_api else " (Mock Mode) 🎭")
    
    if st.button(button_text, type="primary", use_container_width=True):
        spinner_text = "🤖 Calling Real ChatGPT API..." if use_real_api else "⚡ Running tests with mock responses..."
        
        with st.spinner(spinner_text):
            if use_real_api:
                # Create example test class with REAL OpenAI
                class DemoAgentTest(AgentTest):
                    """Demo test suite with REAL ChatGPT"""
                    
                    def setup(self):
                        # Use REAL OpenAI API
                        self.client = OpenAI(api_key=OPENAI_API_KEY)
                        self.responses = []
                    
                    def get_real_response(self, prompt):
                        """Get REAL response from ChatGPT"""
                        start = time.time()
                        try:
                            response = self.client.chat.completions.create(
                                model=OPENAI_MODEL,
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=100
                            )
                        except Exception as e:
                            if "insufficient_quota" in str(e):
                                raise Exception("❌ No OpenAI credits! Add credits at: https://platform.openai.com/settings/organization/billing/overview")
                            raise
                        duration = time.time() - start
                        
                        result = type('Response', (), {
                            'content': response.choices[0].message.content,
                            'tokens_used': response.usage.total_tokens,
                            'cost': response.usage.total_tokens * 0.00000015,  # gpt-4o-mini cost
                            'latency': duration,
                            'model': OPENAI_MODEL,
                        })()
                        
                        self.responses.append({
                            'prompt': prompt,
                            'response': result.content,
                            'tokens': result.tokens_used,
                            'cost': result.cost
                        })
                        
                        return result
                    
                    @test_agent
                    def test_math_query(self):
                        """Test simple math question with REAL ChatGPT"""
                        result = self.get_real_response("What is 2+2? Answer briefly.")
                        self.assert_contains(result.content, "4")
                        st.info(f"💬 ChatGPT: {result.content}")
                    
                    @test_agent
                    def test_geography_query(self):
                        """Test geography question with REAL ChatGPT"""
                        result = self.get_real_response("What is the capital of France? Answer in one word.")
                        self.assert_contains(result.content, "Paris", case_sensitive=False)
                        st.info(f"💬 ChatGPT: {result.content}")
                    
                    @test_agent
                    def test_response_time(self):
                        """Test response latency with REAL ChatGPT"""
                        start = time.time()
                        result = self.get_real_response("Say hello in 3 words.")
                        duration = time.time() - start
                        self.assert_latency(duration, max_seconds=10.0)  # More time for real API
                        st.info(f"💬 ChatGPT: {result.content}")
            else:
                # Create example test class with MOCK (Free)
                class DemoAgentTest(AgentTest):
                    """Demo test suite with Mock LLM"""
                    
                    def setup(self):
                        self.mock = MockLLM()
                        self.mock.add_response(
                            "What is 2+2?",
                            mock_llm_response("The answer is 4", tokens_used=20, cost=0.001)
                        )
                        self.mock.add_response(
                            "What is the capital of France?",
                            mock_llm_response("The capital of France is Paris", tokens_used=30, cost=0.002)
                        )
                        self.mock.add_response(
                            "Say hello",
                            mock_llm_response("Hello! How can I help you today?", tokens_used=25, cost=0.0015)
                        )
                    
                    @test_agent
                    def test_math_query(self):
                        """Test simple math question"""
                        result = self.mock.get_response("What is 2+2?")
                        self.assert_contains(result.content, "4")
                        self.assert_cost(result.cost, max_cost=0.01)
                    
                    @test_agent
                    def test_geography_query(self):
                        """Test geography question"""
                        result = self.mock.get_response("What is the capital of France?")
                        self.assert_contains(result.content, "Paris", case_sensitive=False)
                    
                    @test_agent
                    def test_response_time(self):
                        """Test response latency"""
                        start = time.time()
                        result = self.mock.get_response("Say hello")
                        duration = time.time() - start
                        self.assert_latency(duration, max_seconds=1.0)
            
            # Run tests
            test_instance = DemoAgentTest()
            results = []
            
            for method_name in dir(test_instance):
                if method_name.startswith("test_"):
                    method = getattr(test_instance, method_name)
                    if hasattr(method, "_is_agent_test"):
                        # Create a wrapper that doesn't pass self again
                        def test_wrapper(inst=test_instance, m=method):
                            return m()
                        result = test_instance.run_test(test_wrapper)
                        result.test_name = method_name  # Keep original name
                        results.append(result)
            
            # Update stats
            if 'tests_run' not in st.session_state:
                st.session_state.tests_run = 0
            st.session_state.tests_run += len(results)
            
            # Display results
            st.success(f"✅ Ran {len(results)} tests")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            passed = sum(1 for r in results if r.status == "passed")
            failed = sum(1 for r in results if r.status == "failed")
            total_duration = sum(r.duration for r in results)
            
            with col1:
                st.metric("Total Tests", len(results))
            with col2:
                st.metric("Passed", passed, delta=passed)
            with col3:
                st.metric("Failed", failed, delta=-failed if failed > 0 else 0)
            with col4:
                st.metric("Duration", f"{total_duration:.2f}s")
            
            # Detailed results
            st.markdown("### 📋 Test Results")
            
            for result in results:
                if result.status == "passed":
                    with st.expander(f"✅ {result.test_name} - PASSED ({result.duration:.2f}s)", expanded=False):
                        st.markdown(f"**Duration:** {result.duration:.2f}s")
                        st.markdown(f"**Status:** {result.status}")
                        if result.metadata.get("test_doc"):
                            st.markdown(f"**Description:** {result.metadata['test_doc']}")
                else:
                    with st.expander(f"❌ {result.test_name} - FAILED ({result.duration:.2f}s)", expanded=True):
                        st.error(f"**Error:** {result.error}")
                        st.markdown(f"**Duration:** {result.duration:.2f}s")
            
            # Show call history
            if use_real_api:
                st.markdown("### 📞 Real ChatGPT API Call History")
                call_data = []
                total_cost = 0
                total_tokens = 0
                
                for i, call in enumerate(test_instance.responses):
                    call_data.append({
                        "Call #": i + 1,
                        "Prompt": call["prompt"][:40] + "..." if len(call["prompt"]) > 40 else call["prompt"],
                        "Response": call["response"][:50] + "..." if len(call["response"]) > 50 else call["response"],
                        "Tokens": call["tokens"],
                        "Cost": f"${call['cost']:.6f}"
                    })
                    total_cost += call['cost']
                    total_tokens += call['tokens']
                
                if call_data:
                    st.dataframe(call_data, use_container_width=True)
                    
                    # Show totals
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total API Calls", len(call_data))
                    with col2:
                        st.metric("Total Tokens", total_tokens)
                    with col3:
                        st.metric("Total Cost", f"${total_cost:.6f}")
                    
                    st.info(f"🤖 Model: {OPENAI_MODEL} | ⚡ REAL ChatGPT responses!")
            else:
                st.markdown("### 📞 Mock LLM Call History")
                call_data = []
                for i, call in enumerate(test_instance.mock.call_history):
                    call_data.append({
                        "Call #": i + 1,
                        "Prompt": call["prompt"][:50] + "..." if len(call["prompt"]) > 50 else call["prompt"],
                    })
                
                if call_data:
                    st.dataframe(call_data, use_container_width=True)
                    st.success("🎭 FREE Mock Mode - No API costs!")
            
            st.balloons()

elif page == "Example Tests":
    st.markdown("## 📚 Example Test Suites")
    
    tab1, tab2, tab3 = st.tabs(["Basic Tests", "Mock Tests", "Advanced Tests"])
    
    with tab1:
        st.markdown("### Basic Agent Testing")
        st.code("""
from praisonai_test import AgentTest, test_agent

class TestChatbot(AgentTest):
    '''Test chatbot responses'''
    
    def setup(self):
        # Initialize your chatbot
        self.chatbot = MyChatbot()
    
    @test_agent
    def test_greeting(self):
        '''Test chatbot greets users'''
        response = self.chatbot.chat("Hello")
        
        self.assert_contains(response, "hi", case_sensitive=False)
        self.assert_contains(response, "help")
    
    @test_agent
    def test_response_time(self):
        '''Test chatbot responds quickly'''
        import time
        
        start = time.time()
        response = self.chatbot.chat("Hello")
        duration = time.time() - start
        
        self.assert_latency(duration, max_seconds=2.0)
""", language="python")
    
    with tab2:
        st.markdown("### Testing with Mocks")
        st.code("""
from praisonai_test import AgentTest, test_agent, MockLLM

class TestWithMock(AgentTest):
    '''Test using mocked LLM'''
    
    def setup(self):
        self.mock = MockLLM()
        
        # Add exact match
        self.mock.add_response(
            "What is 2+2?",
            "The answer is 4"
        )
        
        # Add pattern match
        self.mock.add_pattern(
            r".*capital.*",
            "That's a geography question"
        )
    
    @test_agent
    def test_math_question(self):
        '''Test math query with mock'''
        result = self.mock.get_response("What is 2+2?")
        self.assert_contains(result.content, "4")
    
    @test_agent
    def test_geography_question(self):
        '''Test geography query with pattern'''
        result = self.mock.get_response("What is the capital?")
        self.assert_contains(result.content, "geography")
""", language="python")
    
    with tab3:
        st.markdown("### Advanced Testing")
        st.code("""
from praisonai_test import AgentTest, test_agent, parametrize
from praisonai_test.assertions import assert_no_pii, assert_no_hallucination

class TestAdvanced(AgentTest):
    '''Advanced testing features'''
    
    @parametrize([
        {"input": "2+2", "expected": "4"},
        {"input": "3+3", "expected": "6"},
    ])
    @test_agent
    def test_multiple_math(self, input, expected):
        '''Test with multiple parameters'''
        result = self.agent.run(input)
        self.assert_contains(result, expected)
    
    @test_agent
    def test_no_pii_leak(self):
        '''Test for PII leakage'''
        result = self.agent.run("process user data")
        assert_no_pii(result)
    
    @test_agent
    def test_grounded_response(self):
        '''Test response is grounded in sources'''
        sources = ["Document 1 content", "Document 2 content"]
        result = self.agent.run("summarize")
        assert_no_hallucination(result, sources, threshold=0.7)
""", language="python")

elif page == "Create Test":
    st.markdown("## 🔨 Create Your Own Test")
    
    # Example templates
    # Show example tests first
    with st.expander("👀 View Example Generated Tests", expanded=False):
        example_tab = st.tabs(["Chatbot", "Summarization", "Code Gen", "Data Extraction"])
        
        with example_tab[0]:
            st.markdown("**Chatbot Test Example**")
            st.code('''from praisonai_test import AgentTest, test_agent, MockLLM, mock_llm_response

class TestChatbot(AgentTest):
    """Test chatbot conversation flows"""
    
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "Hello! How are you?",
            mock_llm_response("Hello! I'm doing great, thanks for asking!", tokens_used=50)
        )
    
    @test_agent
    def test_greeting_response(self):
        """Test chatbot responds to greetings appropriately"""
        result = self.mock.get_response("Hello! How are you?")
        
        self.assert_contains(result.content, "hello")
        self.assert_latency(result.latency, max_seconds=2.0)
        self.assert_cost(result.cost, max_cost=0.10)
''', language="python")
        
        with example_tab[1]:
            st.markdown("**Summarization Test Example**")
            st.code('''from praisonai_test import AgentTest, test_agent, MockLLM, mock_llm_response

class TestSummarizer(AgentTest):
    """Test document summarization agent"""
    
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "Summarize: PraisonAI is a testing framework for AI agents",
            mock_llm_response("PraisonAI: AI agent testing framework", tokens_used=30)
        )
    
    @test_agent
    def test_summary_quality(self):
        """Test that summary contains key points"""
        result = self.mock.get_response("Summarize: PraisonAI is a testing framework for AI agents")
        
        self.assert_contains(result.content, "PraisonAI")
        self.assert_contains(result.content, "testing")
''', language="python")
        
        with example_tab[2]:
            st.markdown("**Code Generator Test Example**")
            st.code('''from praisonai_test import AgentTest, test_agent, MockLLM, mock_llm_response

class TestCodeGen(AgentTest):
    """Test AI code generation agent"""
    
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "Write a Python function to add two numbers",
            mock_llm_response("def add(a, b):\\n    return a + b", tokens_used=80)
        )
    
    @test_agent
    def test_python_function(self):
        """Test generating a Python function"""
        result = self.mock.get_response("Write a Python function to add two numbers")
        
        self.assert_contains(result.content, "def")
        self.assert_contains(result.content, "return")
''', language="python")
        
        with example_tab[3]:
            st.markdown("**Data Extraction Test Example**")
            st.code('''from praisonai_test import AgentTest, test_agent, MockLLM, mock_llm_response
from praisonai_test.assertions import assert_no_pii

class TestDataExtractor(AgentTest):
    """Test data extraction from text"""
    
    def setup(self):
        self.mock = MockLLM()
        self.mock.add_response(
            "Extract email from: Contact us at info@example.com",
            mock_llm_response("Email: info@example.com", tokens_used=40)
        )
    
    @test_agent
    def test_extract_email(self):
        """Test extracting email from text"""
        result = self.mock.get_response("Extract email from: Contact us at info@example.com")
        
        self.assert_contains(result.content, "info@example.com")
        # Verify no PII leakage in other parts
        assert_no_pii(result.content.replace("info@example.com", "[EMAIL]"))
''', language="python")
    
    st.markdown("---")
    st.markdown("### 📝 Quick Templates")
    
    templates = {
        "Custom": {
            "test_name": "TestMyAgent",
            "description": "Test suite for my AI agent",
            "method_name": "test_simple_query",
            "method_doc": "Test basic agent query",
            "prompt": "What is 2+2?",
            "expected": "4",
            "use_mock": True,
        },
        "Chatbot": {
            "test_name": "TestChatbot",
            "description": "Test chatbot conversation flows",
            "method_name": "test_greeting_response",
            "method_doc": "Test chatbot responds to greetings appropriately",
            "prompt": "Hello! How are you?",
            "expected": "hello",
            "use_mock": True,
        },
        "Summarization": {
            "test_name": "TestSummarizer",
            "description": "Test document summarization agent",
            "method_name": "test_summary_quality",
            "method_doc": "Test that summary contains key points",
            "prompt": "Summarize: PraisonAI is a testing framework for AI agents",
            "expected": "PraisonAI",
            "use_mock": True,
        },
        "Code Generator": {
            "test_name": "TestCodeGen",
            "description": "Test AI code generation agent",
            "method_name": "test_python_function",
            "method_doc": "Test generating a Python function",
            "prompt": "Write a Python function to add two numbers",
            "expected": "def",
            "use_mock": True,
        },
        "Data Extraction": {
            "test_name": "TestDataExtractor",
            "description": "Test data extraction from text",
            "method_name": "test_extract_email",
            "method_doc": "Test extracting email from text",
            "prompt": "Extract email from: Contact us at info@example.com",
            "expected": "info@example.com",
            "use_mock": True,
        },
        "Q&A Agent": {
            "test_name": "TestQAAgent",
            "description": "Test question answering agent",
            "method_name": "test_factual_answer",
            "method_doc": "Test answering factual questions",
            "prompt": "What is the capital of France?",
            "expected": "Paris",
            "use_mock": True,
        },
    }
    
    template_choice = st.selectbox(
        "Choose a template to start with:",
        list(templates.keys()),
        help="Select a template or choose 'Custom' to create from scratch"
    )
    
    selected_template = templates[template_choice]
    
    st.markdown("---")
    st.markdown("### ⚙️ Test Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_name = st.text_input("Test Class Name", selected_template["test_name"], help="Name for your test class")
        test_description = st.text_area("Test Description", selected_template["description"])
    
    with col2:
        method_name = st.text_input("Test Method Name", selected_template["method_name"])
        method_doc = st.text_input("Method Description", selected_template["method_doc"])
    
    st.markdown("### 📨 Test Input & Expected Output")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prompt = st.text_area("Test Prompt/Input", selected_template["prompt"], height=100)
        mock_response = st.text_area("Mock Response (for testing)", 
                                     f"Mock response containing: {selected_template['expected']}", 
                                     height=100)
    
    with col2:
        expected_response = st.text_area("Expected in Response", selected_template["expected"], height=100)
        use_mock = st.checkbox("Use Mock LLM (Free - No API needed)", value=True, 
                               help="Mock = Free fake responses. Uncheck to use REAL ChatGPT (requires credits)")
    
    st.markdown("### 🎯 Additional Assertions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_latency = st.checkbox("Check Latency", value=True)
        if check_latency:
            max_latency = st.number_input("Max Latency (seconds)", min_value=0.1, value=2.0, step=0.1)
    
    with col2:
        check_cost = st.checkbox("Check Cost", value=True)
        if check_cost:
            max_cost = st.number_input("Max Cost (USD)", min_value=0.001, value=0.10, step=0.01, format="%.3f")
    
    with col3:
        check_tokens = st.checkbox("Check Tokens", value=False)
        if check_tokens:
            max_tokens = st.number_input("Max Tokens", min_value=1, value=1000, step=100)
    
    st.markdown("### 🛡️ Safety Checks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        check_pii = st.checkbox("Check for PII Leakage", value=False)
    
    with col2:
        check_json = st.checkbox("Validate JSON Format", value=False)
    
    st.markdown("---")
    
    if st.button("🚀 Generate Test Code", type="primary", use_container_width=True):
        # Build imports
        imports = ["from praisonai_test import AgentTest, test_agent"]
        if use_mock:
            imports.append("from praisonai_test import MockLLM, mock_llm_response")
        else:
            imports.append("from openai import OpenAI")
        if check_tokens:
            imports.append("from praisonai_test.assertions import assert_token_count")
        if check_pii:
            imports.append("from praisonai_test.assertions import assert_no_pii")
        if check_latency:
            imports.append("import time")
        
        # Build setup method
        setup_code = '    def setup(self):\n        """Setup before each test"""\n'
        if use_mock:
            setup_code += f'''        # Create mock LLM
        self.mock = MockLLM()
        self.mock.add_response(
            "{prompt}",
            mock_llm_response("{mock_response}", tokens_used=50, cost=0.005)
        )\n'''
        else:
            setup_code += f'''        # Use REAL ChatGPT API
        self.client = OpenAI(api_key="{OPENAI_API_KEY}")
        self.model = "{OPENAI_MODEL}"
        self.responses = []\n'''
        
        # Build test method
        test_method = f'''    @test_agent
    def {method_name}(self):
        """{method_doc}"""
'''
        
        if not use_mock:
            # Add helper method for real API calls
            test_method += f'''        # Get REAL ChatGPT response
        start = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{{"role": "user", "content": "{prompt}"}}],
            max_tokens=150
        )
        result_content = response.choices[0].message.content
        duration = time.time() - start
        tokens = response.usage.total_tokens
        cost = tokens * 0.00000015  # gpt-4o-mini cost
        
        # Store response info
        self.responses.append({{
            'content': result_content,
            'tokens': tokens,
            'cost': cost,
            'latency': duration
        }})
        
        # Assertions
        self.assert_contains(result_content, "{expected_response}")
'''
        else:
            if check_latency:
                test_method += '        import time\n        start = time.time()\n        '
            else:
                test_method += '        '
            
            test_method += f'result = self.mock.get_response("{prompt}")\n'
            
            if check_latency:
                test_method += '        duration = time.time() - start\n'
            
            test_method += '\n        # Assertions\n'
            test_method += f'        self.assert_contains(result.content, "{expected_response}")\n'
        
        if use_mock:
            if check_json:
                test_method += f'        self.assert_json_valid(result.content)\n'
            
            if check_latency:
                test_method += f'        self.assert_latency(result.latency, max_seconds={max_latency})\n'
            
            if check_cost:
                test_method += f'        self.assert_cost(result.cost, max_cost={max_cost})\n'
            
            if check_tokens:
                test_method += f'        assert_token_count(result.tokens_used, max_tokens={max_tokens})\n'
            
            if check_pii:
                test_method += f'        assert_no_pii(result.content)\n'
        else:
            # Real API assertions
            if check_json:
                test_method += f'        self.assert_json_valid(result_content)\n'
            
            if check_latency:
                test_method += f'        self.assert_latency(duration, max_seconds={max_latency})\n'
            
            if check_cost:
                test_method += f'        self.assert_cost(cost, max_cost={max_cost})\n'
            
            if check_tokens:
                test_method += f'        assert_token_count(tokens, max_tokens={max_tokens})\n'
            
            if check_pii:
                test_method += f'        assert_no_pii(result_content)\n'
        
        # Build complete test code
        test_code = f'''"""
{test_description}

Generated with PraisonAI Test Framework
"""

{chr(10).join(imports)}


class {test_name}(AgentTest):
    """{test_description}"""
    
{setup_code}
{test_method}

# Run the test
if __name__ == "__main__":
    import pytest
    
    # Option 1: Run with pytest
    pytest.main([__file__, "-v"])
    
    # Option 2: Run directly
    # test = {test_name}()
    # result = test.run_test(test.{method_name})
    # print(f"Test {{result.status}}: {{result.test_name}}")
    # if result.error:
    #     print(f"Error: {{result.error}}")
'''
        
        st.success("✅ Test code generated successfully!")
        
        # Show summary
        st.markdown("### 📊 Test Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Test Class", test_name)
        with col2:
            st.metric("Test Method", method_name)
        with col3:
            assertions_count = sum([
                1,  # assert_contains (always included)
                check_latency,
                check_cost,
                check_tokens,
                check_pii,
                check_json
            ])
            st.metric("Assertions", assertions_count)
        
        # Show features
        features = []
        if use_mock:
            features.append("🎭 Uses Mock LLM (no API costs)")
        else:
            features.append(f"🤖 Uses REAL ChatGPT ({OPENAI_MODEL})")
        if check_latency:
            features.append(f"⏱️ Latency check (< {max_latency}s)")
        if check_cost:
            features.append(f"💰 Cost check (< ${max_cost})")
        if check_tokens:
            features.append(f"🎯 Token limit ({max_tokens} max)")
        if check_pii:
            features.append("🛡️ PII detection")
        if check_json:
            features.append("📋 JSON validation")
        
        if features:
            st.markdown("**Features included:**")
            for feature in features:
                st.markdown(f"- {feature}")
        
        st.markdown("---")
        
        # Show code with syntax highlighting
        st.markdown("### 💻 Generated Code")
        st.code(test_code, language="python")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                "💾 Download Test File",
                test_code,
                file_name=f"{test_name.lower()}.py",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.toast("Code copied! (Use Ctrl+C on the code block above)")
        
        with col3:
            if st.button("🔄 Generate Another", use_container_width=True):
                st.rerun()
        
        # Add option to run the test live
        st.markdown("---")
        st.markdown("### 🎮 Test Your Generated Code")
        
        if st.button("▶️ Run This Test Live", type="secondary", use_container_width=True):
            with st.spinner("Running your generated test..."):
                try:
                    # Create a namespace to execute the code
                    exec_globals = {
                        'AgentTest': AgentTest,
                        'test_agent': test_agent,
                        'MockLLM': MockLLM,
                        'mock_llm_response': mock_llm_response,
                        'OpenAI': OpenAI,
                        'assert_token_count': assert_token_count if check_tokens else None,
                        'assert_no_pii': assert_no_pii if check_pii else None,
                        'time': time,
                    }
                    
                    # Execute the generated code
                    exec(test_code, exec_globals)
                    
                    # Get the test class
                    test_class = exec_globals[test_name]
                    test_instance = test_class()
                    
                    # Run the test
                    method = getattr(test_instance, method_name)
                    result = test_instance.run_test(lambda: method())
                    result.test_name = method_name
                    
                    # Display result
                    if result.status == "passed":
                        st.success(f"✅ Test PASSED in {result.duration:.3f}s!")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Status", "✅ PASSED")
                        with col2:
                            st.metric("Duration", f"{result.duration:.3f}s")
                        with col3:
                            st.metric("Test", method_name)
                        
                        # Show real API response if not using mock
                        if not use_mock and hasattr(test_instance, 'responses') and test_instance.responses:
                            st.markdown("---")
                            st.markdown("### 🤖 Real ChatGPT Response")
                            for i, resp in enumerate(test_instance.responses):
                                with st.expander(f"💬 Response #{i+1}", expanded=True):
                                    st.markdown(f"**Content:** {resp['content']}")
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Tokens", resp['tokens'])
                                    with col2:
                                        st.metric("Cost", f"${resp['cost']:.6f}")
                                    with col3:
                                        st.metric("Latency", f"{resp['latency']:.2f}s")
                            st.info(f"🤖 Model: {OPENAI_MODEL} | ⚡ REAL ChatGPT response!")
                        
                        st.balloons()
                    else:
                        st.error(f"❌ Test FAILED")
                        st.code(result.error, language="text")
                        
                except Exception as e:
                    st.error(f"❌ Error running test: {str(e)}")
                    with st.expander("See full traceback"):
                        st.code(traceback.format_exc(), language="text")
        
        st.markdown("---")
        
        st.markdown("### 🚀 Next Steps")
        st.markdown("""
        1. **Download** the test file using the button above
        2. **Save** it to your `tests/` directory
        3. **Run** the test:
           ```bash
           # Option 1: Using pytest
           pytest test_file.py -v
           
           # Option 2: Using praisonai-test
           praisonai-test run --path tests/
           
           # Option 3: Run directly
           python test_file.py
           ```
        """)
        
        st.info("💡 **Tip:** Modify the generated code to match your specific agent implementation!")
        
        # Example of running the test
        if st.checkbox("🎬 See example output"):
            st.markdown("**Example test execution output:**")
            st.code(f"""$ pytest {test_name.lower()}.py -v

========================= test session starts =========================
collected 1 item

{test_name.lower()}.py::{test_name}::{method_name} PASSED [100%]

========================== 1 passed in 0.15s ==========================
""", language="bash")

else:  # Documentation
    st.markdown("## 📖 Documentation")
    
    doc_tab = st.tabs(["Installation", "CLI Commands", "Writing Tests", "Assertions", "Mocking"])
    
    with doc_tab[0]:
        st.markdown("### 💿 Installation")
        st.code("pip install praisonai-test", language="bash")
        
        st.markdown("### 📦 Verify Installation")
        st.code("praisonai-test --version", language="bash")
    
    with doc_tab[1]:
        st.markdown("### 🖥️ CLI Commands")
        
        commands = {
            "Create new test": "praisonai-test new my-tests",
            "Run all tests": "praisonai-test run",
            "Run with verbose": "praisonai-test run -v",
            "Generate HTML report": "praisonai-test run --report html --output report.html",
            "Generate JUnit XML": "praisonai-test run --report junit --output junit.xml",
            "Initialize in project": "praisonai-test init",
            "Show version": "praisonai-test version",
        }
        
        for desc, cmd in commands.items():
            st.markdown(f"**{desc}:**")
            st.code(cmd, language="bash")
    
    with doc_tab[2]:
        st.markdown("### ✍️ Writing Tests")
        
        st.markdown("#### Basic Structure")
        st.code("""
from praisonai_test import AgentTest, test_agent

class TestMyAgent(AgentTest):
    def setup(self):
        # Setup code
        pass
    
    @test_agent
    def test_something(self):
        # Test code
        pass
    
    def teardown(self):
        # Cleanup code
        pass
""", language="python")
    
    with doc_tab[3]:
        st.markdown("### ✅ Assertions")
        
        assertions = {
            "Content": [
                "self.assert_contains(output, 'text')",
                "self.assert_not_contains(output, 'text')",
                "self.assert_equals(actual, expected)",
            ],
            "Format": [
                "self.assert_json_valid(output)",
                "assert_format(output, 'json')",
            ],
            "Performance": [
                "self.assert_latency(duration, max_seconds=2.0)",
                "self.assert_cost(cost, max_cost=0.10)",
                "assert_token_count(tokens, max_tokens=1000)",
            ],
            "Safety": [
                "assert_no_pii(output)",
                "assert_no_hallucination(output, sources)",
            ],
        }
        
        for category, methods in assertions.items():
            st.markdown(f"#### {category}")
            for method in methods:
                st.code(method, language="python")
    
    with doc_tab[4]:
        st.markdown("### 🎭 Mocking")
        
        st.markdown("#### Create Mock")
        st.code("""
from praisonai_test import MockLLM, mock_llm_response

mock = MockLLM()

# Exact match
mock.add_response("prompt", "response")

# Pattern match
mock.add_pattern(r".*question.*", "answer")

# Function match
def matcher(prompt, **kwargs):
    return "keyword" in prompt

mock.add_function_response(matcher, "response")
""", language="python")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Built with ❤️ by the PraisonAI Team</p>
    <p>
        <a href="https://github.com/MervinPraison/PraisonAI-Test">GitHub</a> • 
        <a href="https://praison.ai">Website</a> • 
        <a href="https://github.com/MervinPraison/PraisonAI-Test/issues">Issues</a>
    </p>
</div>
""", unsafe_allow_html=True)

