"""
Tests for PromptTransformer module.

This module tests the new lightweight PromptTransformer that replaces
the complex PromptInterpreter, focusing on prompt enhancement rather
than structured command parsing.
"""

import pytest
from prompt_transformer import PromptTransformer


class TestPromptTransformer:
    """Test cases for PromptTransformer functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.transformer = PromptTransformer()
    
    def test_enhance_simple_prompt(self):
        """Test basic prompt enhancement functionality."""
        user_prompt = "Find posts about AI"
        enhanced = self.transformer.enhance_prompt(user_prompt)
        
        # Enhanced prompt should contain original prompt
        assert user_prompt in enhanced
        # Should add LinkedIn context
        assert "LinkedIn" in enhanced
        # Should maintain reasonable length
        assert len(enhanced) > len(user_prompt)
        assert len(enhanced) < 1000  # Reasonable upper limit
    
    def test_enhance_empty_prompt(self):
        """Test validation of empty prompts."""
        with pytest.raises(ValueError, match="Empty prompt"):
            self.transformer.enhance_prompt("")
        
        with pytest.raises(ValueError, match="Empty prompt"):
            self.transformer.enhance_prompt("   ")  # Whitespace only
    
    def test_enhance_none_prompt(self):
        """Test validation of None input."""
        with pytest.raises(ValueError, match="Empty prompt"):
            self.transformer.enhance_prompt(None)
    
    def test_enhance_complex_prompt(self):
        """Test enhancement of complex multi-step prompts."""
        complex_prompt = "Find AI researchers at YC companies and engage thoughtfully with their recent posts"
        enhanced = self.transformer.enhance_prompt(complex_prompt)
        
        # Should preserve the complex instruction
        assert "AI researchers" in enhanced
        assert "YC companies" in enhanced
        assert "engage thoughtfully" in enhanced
        # Should add professional conduct guidance
        assert "professional" in enhanced.lower() or "respectful" in enhanced.lower()
    
    def test_enhance_maintains_intent(self):
        """Test that enhancement preserves user intent."""
        test_cases = [
            "Like posts about machine learning",
            "Comment on startup funding discussions", 
            "Share insights about remote work trends",
            "Find people working in fintech"
        ]
        
        for user_prompt in test_cases:
            enhanced = self.transformer.enhance_prompt(user_prompt)
            # Original keywords should be preserved
            key_words = user_prompt.lower().split()
            for word in key_words:
                if len(word) > 3:  # Skip short words like "in", "on"
                    assert word in enhanced.lower()
    
    def test_enhance_adds_safety_guidelines(self):
        """Test that enhancement adds appropriate safety guidelines."""
        user_prompt = "Comment on controversial posts"
        enhanced = self.transformer.enhance_prompt(user_prompt)
        
        # Should include professional conduct guidance
        safety_indicators = [
            "professional", "respectful", "appropriate", 
            "constructive", "thoughtful", "considerate"
        ]
        has_safety_guidance = any(indicator in enhanced.lower() for indicator in safety_indicators)
        assert has_safety_guidance, f"Enhanced prompt should include safety guidance: {enhanced}"
    
    def test_enhance_handles_long_prompts(self):
        """Test handling of very long prompts."""
        long_prompt = "Find posts about artificial intelligence " * 20  # Very long prompt
        enhanced = self.transformer.enhance_prompt(long_prompt)
        
        # Should handle long prompts without error
        assert isinstance(enhanced, str)
        assert len(enhanced) > 0
        # Should still contain core instruction
        assert "artificial intelligence" in enhanced
    
    def test_enhance_is_deterministic(self):
        """Test that enhancement is deterministic for the same input."""
        user_prompt = "Find posts about blockchain technology"
        enhanced1 = self.transformer.enhance_prompt(user_prompt)
        enhanced2 = self.transformer.enhance_prompt(user_prompt)
        
        # Should produce consistent results
        assert enhanced1 == enhanced2
    
    def test_enhance_different_prompts_different_results(self):
        """Test that different prompts produce different enhanced results."""
        prompt1 = "Find posts about AI"
        prompt2 = "Like posts about blockchain"
        
        enhanced1 = self.transformer.enhance_prompt(prompt1)
        enhanced2 = self.transformer.enhance_prompt(prompt2)
        
        # Different prompts should produce different enhancements
        assert enhanced1 != enhanced2
        assert "AI" in enhanced1
        assert "blockchain" in enhanced2
