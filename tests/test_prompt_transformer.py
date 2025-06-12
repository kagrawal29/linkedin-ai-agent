"""
Tests for PromptTransformer module.

This module tests the new lightweight PromptTransformer that replaces
the complex PromptInterpreter with a simple enhancement approach
optimized for browser-use Agent.
"""

import pytest
from unittest.mock import patch, MagicMock
from prompt_transformer import PromptTransformer


class TestPromptTransformer:
    """Test cases for PromptTransformer functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transformer = PromptTransformer()
    
    def test_enhance_prompt_basic_functionality(self):
        """Test basic prompt enhancement functionality."""
        user_prompt = "like 3 posts about AI"
        enhanced = self.transformer.enhance_prompt(user_prompt)
        
        assert isinstance(enhanced, str)
        assert len(enhanced) > len(user_prompt)
        assert "LinkedIn" in enhanced
        assert "professional" in enhanced.lower()
    
    def test_enhance_prompt_empty_input_validation(self):
        """Test that empty prompts raise ValueError."""
        with pytest.raises(ValueError, match="Empty prompt not allowed"):
            self.transformer.enhance_prompt("")
        
        with pytest.raises(ValueError, match="Empty prompt not allowed"):
            self.transformer.enhance_prompt(None)
        
        with pytest.raises(ValueError, match="Empty prompt not allowed"):
            self.transformer.enhance_prompt("   ")
    
    def test_clean_prompt_whitespace_normalization(self):
        """Test prompt cleaning and normalization."""
        test_cases = [
            ("  like    posts   about  AI  ", "Like posts about AI"),
            ("hello world", "Hello world"),
            ("ALREADY CAPITALIZED", "ALREADY CAPITALIZED"),
            ("multiple\n\nlines\tand\tspaces", "Multiple lines and spaces")
        ]
        
        for input_prompt, expected in test_cases:
            cleaned = self.transformer._clean_prompt(input_prompt)
            assert cleaned == expected
    
    def test_build_enhanced_prompt_structure(self):
        """Test the structure of enhanced prompts."""
        clean_prompt = "Like 3 posts about AI"
        enhanced = self.transformer._build_enhanced_prompt(clean_prompt)
        
        # Check that all required sections are present
        assert "LinkedIn" in enhanced
        assert "Task: Like 3 posts about AI" in enhanced
        assert "guidelines:" in enhanced
        assert "professional" in enhanced
        assert len(enhanced.split('\n')) > 5  # Multi-line structure

    # === CYCLE 3: TEMPLATE ENGINE INTEGRATION TESTS ===
    
    def test_template_engine_initialization(self):
        """RED: Test PromptTransformer initializes PromptTemplateEngine when use_templates=True."""
        # This should fail because PromptTransformer doesn't have use_templates parameter yet
        transformer = PromptTransformer(use_templates=True)
        assert hasattr(transformer, 'template_engine'), "PromptTemplateEngine not initialized"
        assert transformer.template_engine is not None
    
    def test_template_detection_and_rendering(self):
        """RED: Test template detection and enhanced rendering for LinkedIn actions."""
        transformer = PromptTransformer(use_templates=True)
        
        # Test cases that should trigger template rendering
        template_test_cases = [
            "Like 3 posts about AI",
            "Comment 'Great insights!' on recent posts about startups", 
            "Connect with 5 people from Google",
            "Find posts about machine learning"
        ]
        
        for prompt in template_test_cases:
            enhanced = transformer.enhance_prompt(prompt)
            # Should contain numbered steps from template rendering
            assert any(char.isdigit() and ". " in enhanced for char in enhanced), f"No numbered steps found in template for: {prompt}"
            assert "Navigate to LinkedIn" in enhanced, f"Template steps missing for: {prompt}"
    
    def test_fallback_to_generic_enhancement(self):
        """RED: Test fallback to generic enhancement when no template matches."""
        transformer = PromptTransformer(use_templates=True)
        
        # Prompts that shouldn't match any template
        non_template_prompts = [
            "Tell me about your day",
            "What's the weather like?", 
            "Random unrelated content"
        ]
        
        for prompt in non_template_prompts:
            enhanced = transformer.enhance_prompt(prompt)
            # Should fall back to generic enhancement (no numbered steps)
            assert "LinkedIn" in enhanced, "Generic LinkedIn context missing"
            assert "professional" in enhanced.lower(), "Professional guidelines missing"
            # Should NOT have template-style numbered steps
            steps_count = len([line for line in enhanced.split('\n') if line.strip() and line.strip()[0].isdigit() and '. ' in line])
            assert steps_count == 0, f"Unexpected template steps found for non-template prompt: {prompt}"
    
    @patch('prompt_transformer.PromptTemplateEngine')
    def test_llm_integration_toggle(self, mock_template_engine_class):
        """RED: Test LLM integration can be enabled/disabled in PromptTransformer."""
        mock_engine = MagicMock()
        mock_template_engine_class.return_value = mock_engine
        
        # Test with LLM enabled
        transformer = PromptTransformer(use_templates=True, use_llm=True)
        transformer.enhance_prompt("Like posts about AI")
        
        # Verify PromptTemplateEngine was initialized with LLM enabled
        mock_template_engine_class.assert_called_with(use_llm=True)
    
    def test_immediate_response_capability(self):
        """RED: Test PromptTransformer can return enhanced prompt immediately."""
        transformer = PromptTransformer(use_templates=True)
        
        prompt = "Like 3 posts about AI"
        enhanced = transformer.enhance_prompt(prompt)
        
        # Enhanced prompt should be available immediately (synchronous)
        assert enhanced is not None
        assert isinstance(enhanced, str)
        assert len(enhanced) > 0
        # Should not block or require async execution
        
    def test_template_vs_generic_enhancement_quality(self):
        """RED: Test template-enhanced prompts are more detailed than generic ones."""
        transformer_with_templates = PromptTransformer(use_templates=True)
        transformer_generic = PromptTransformer(use_templates=False)
        
        linkedin_prompt = "Like 5 posts about startups"
        
        template_enhanced = transformer_with_templates.enhance_prompt(linkedin_prompt)
        generic_enhanced = transformer_generic.enhance_prompt(linkedin_prompt)
        
        # Template version should be more detailed
        assert len(template_enhanced) > len(generic_enhanced), "Template enhancement should be more detailed"
        
        # Template version should have specific action steps
        template_steps = len([line for line in template_enhanced.split('\n') if line.strip() and line.strip()[0].isdigit() and '. ' in line])
        generic_steps = len([line for line in generic_enhanced.split('\n') if line.strip() and line.strip()[0].isdigit() and '. ' in line])
        
        assert template_steps > generic_steps, "Template should provide more specific action steps"
    
    def test_error_handling_with_template_engine_failure(self):
        """RED: Test graceful fallback when template engine fails."""
        with patch('prompt_transformer.PromptTemplateEngine') as mock_template_class:
            # Mock template engine to raise an exception
            mock_engine = MagicMock()
            mock_engine.detect_intent.side_effect = Exception("Template engine error")
            mock_template_class.return_value = mock_engine
            
            transformer = PromptTransformer(use_templates=True)
            enhanced = transformer.enhance_prompt("Like posts about AI")
            
            # Should gracefully fall back to generic enhancement
            assert enhanced is not None
            assert "LinkedIn" in enhanced
            assert len(enhanced) > 0
    
    def test_parameter_extraction_integration(self):
        """RED: Test parameter extraction from PromptTemplateEngine is used in enhancement."""
        transformer = PromptTransformer(use_templates=True)
        
        complex_prompt = "Like 5 posts about artificial intelligence from Sundar Pichai"
        enhanced = transformer.enhance_prompt(complex_prompt)
        
        # Enhanced prompt should incorporate extracted parameters
        assert "5" in enhanced, "Count parameter not incorporated"
        assert "artificial intelligence" in enhanced.lower(), "Keywords not incorporated" 
        assert "Sundar Pichai" in enhanced, "Target person not incorporated"
