"""
Test cases for enhanced prompt generation with detailed browser automation scripts.

Tests the PromptTransformer's ability to generate sophisticated browser automation
instructions for common LinkedIn actions.
"""

import unittest
from prompt_transformer import PromptTransformer


class TestEnhancedPromptGeneration(unittest.TestCase):
    """Test enhanced prompt generation capabilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.transformer = PromptTransformer(use_templates=False, use_llm=False)
    
    def test_like_action_detection(self):
        """Test that 'like' actions generate detailed engagement instructions."""
        prompt = "like the first fundraising related post on my feed"
        enhanced = self.transformer.enhance_prompt(prompt)
        
        # Should contain detailed steps, not just basic "1. Navigate to LinkedIn"
        self.assertIn("DETAILED BROWSER AUTOMATION PLAN", enhanced)
        self.assertIn("ENGAGEMENT PHASE", enhanced)
        self.assertIn("LinkedIn DOM HINTS", enhanced)
        self.assertIn("button[aria-label*=\"Like\"]", enhanced)
        
        # Should still maintain safety guidelines
        self.assertIn("SAFETY GUIDELINES", enhanced)
        self.assertIn("professional and respectful tone", enhanced)
    
    def test_connect_action_detection(self):
        """Test that 'connect' actions generate search and connection instructions."""
        prompt = "Connect with 2 software engineers at Google working on AI"
        enhanced = self.transformer.enhance_prompt(prompt)
        
        # Should contain search and connection phases
        self.assertIn("SEARCH PHASE", enhanced)
        self.assertIn("CONNECTION PHASE", enhanced)
        self.assertIn("Google", enhanced)
        self.assertIn("AI", enhanced)
        self.assertIn("personalized connection messages", enhanced)
    
    def test_comment_action_detection(self):
        """Test that 'comment' actions generate research and composition instructions."""
        prompt = "comment on AI posts from tech leaders"
        enhanced = self.transformer.enhance_prompt(prompt)
        
        # Should contain research and comment phases
        self.assertIn("RESEARCH PHASE", enhanced)
        self.assertIn("COMMENT COMPOSITION", enhanced)
        self.assertIn("thoughtful, value-adding comments", enhanced)
    
    def test_generic_fallback_still_works(self):
        """Test that non-specific prompts still get basic enhancement."""
        prompt = "help me with some LinkedIn task"
        enhanced = self.transformer.enhance_prompt(prompt)
        
        # Should still contain LinkedIn context and safety guidelines
        self.assertIn("You are working on LinkedIn", enhanced)
        self.assertIn("SAFETY GUIDELINES", enhanced)
        self.assertIn("thoughtful engagement", enhanced)
    
    def test_maintains_original_task(self):
        """Test that original task is preserved in enhanced prompt."""
        original_prompt = "like the first fundraising related post on my feed"
        enhanced = self.transformer.enhance_prompt(original_prompt)
        
        # Original task should be clearly stated (note: gets capitalized)
        self.assertIn(f"Original Task: {original_prompt.capitalize()}", enhanced)


if __name__ == '__main__':
    unittest.main()
