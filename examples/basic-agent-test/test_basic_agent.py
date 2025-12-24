"""
Example: Basic AI Agent Testing
"""

from praisonai_test import AgentTest, test_agent, skip_test, parametrize


class TestBasicAgent(AgentTest):
    """Example test suite for a basic AI agent"""
    
    def setup(self):
        """Setup before each test"""
        # In a real scenario, you would initialize your agent here
        # self.agent = MyAgent(model="gpt-4")
        
        # For this example, we'll simulate responses
        self.simulated_responses = {
            "What is 2+2?": "The answer is 4",
            "What is the capital of France?": "The capital of France is Paris",
            "Tell me a joke": "Why did the chicken cross the road? To get to the other side!",
        }
    
    def teardown(self):
        """Cleanup after each test"""
        pass
    
    @test_agent
    def test_simple_math_query(self):
        """Test agent can answer simple math questions"""
        # Simulate agent call
        result = self.simulated_responses["What is 2+2?"]
        
        # Assertions
        self.assert_contains(result, "4")
        self.assert_not_contains(result, "error")
    
    @test_agent
    def test_geography_query(self):
        """Test agent can answer geography questions"""
        result = self.simulated_responses["What is the capital of France?"]
        
        self.assert_contains(result, "Paris", case_sensitive=False)
        self.assert_contains(result, "France")
    
    @test_agent
    def test_creative_query(self):
        """Test agent can generate creative content"""
        result = self.simulated_responses["Tell me a joke"]
        
        # Check that response is not empty
        assert len(result) > 10, "Response too short"
        
        # Check for common joke patterns
        self.assert_similarity(result, "joke question answer", min_score=0.3)
    
    @parametrize([
        {"query": "What is 2+2?", "expected": "4"},
        {"query": "What is the capital of France?", "expected": "Paris"},
    ])
    @test_agent
    def test_multiple_queries(self, query, expected):
        """Test agent with multiple queries"""
        result = self.simulated_responses.get(query, "Unknown")
        self.assert_contains(result, expected, case_sensitive=False)
    
    @test_agent
    def test_response_format(self):
        """Test agent response is properly formatted"""
        result = self.simulated_responses["What is 2+2?"]
        
        # Check basic formatting
        assert isinstance(result, str), "Response should be a string"
        assert len(result.strip()) > 0, "Response should not be empty"
    
    @skip_test("Feature not implemented yet")
    @test_agent
    def test_future_feature(self):
        """Test future feature"""
        pass


class TestAgentPerformance(AgentTest):
    """Test suite for agent performance metrics"""
    
    @test_agent
    def test_response_latency(self):
        """Test agent responds within acceptable time"""
        import time
        
        start = time.time()
        # Simulate agent processing
        time.sleep(0.1)
        result = "Quick response"
        duration = time.time() - start
        
        # Assert latency is acceptable
        self.assert_latency(duration, max_seconds=1.0)
    
    @test_agent
    def test_token_efficiency(self):
        """Test agent uses tokens efficiently"""
        # Simulate token counting
        prompt_tokens = 50
        completion_tokens = 100
        total_tokens = prompt_tokens + completion_tokens
        
        # Check token usage is reasonable
        from praisonai_test.assertions import assert_token_count
        assert_token_count(total_tokens, max_tokens=500)
    
    @test_agent
    def test_cost_efficiency(self):
        """Test agent cost is within budget"""
        # Simulate cost calculation (e.g., $0.03 per 1K tokens)
        tokens = 1000
        cost_per_1k = 0.03
        total_cost = (tokens / 1000) * cost_per_1k
        
        # Assert cost is acceptable
        self.assert_cost(total_cost, max_cost=0.10)


class TestAgentSafety(AgentTest):
    """Test suite for agent safety and compliance"""
    
    @test_agent
    def test_no_pii_in_response(self):
        """Test agent doesn't leak PII"""
        result = "The user's information has been processed successfully."
        
        from praisonai_test.assertions import assert_no_pii
        assert_no_pii(result)
    
    @test_agent
    def test_no_hallucination(self):
        """Test agent response is grounded in source"""
        source_docs = [
            "PraisonAI is an AI agent testing framework.",
            "It provides mocking, assertions, and CI/CD integration.",
        ]
        
        result = "PraisonAI is a testing framework for AI agents with CI/CD support."
        
        from praisonai_test.assertions import assert_no_hallucination
        assert_no_hallucination(result, source_docs, threshold=0.5)

