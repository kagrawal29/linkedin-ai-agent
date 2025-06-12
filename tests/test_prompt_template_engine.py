import unittest
from unittest.mock import patch, MagicMock

class TestPromptTemplateEngine(unittest.TestCase):

    def test_engine_initialization(self):
        """RED: Test that the PromptTemplateEngine can be initialized."""
        try:
            from prompt_template_engine import PromptTemplateEngine
            engine = PromptTemplateEngine()
            self.assertIsInstance(engine, PromptTemplateEngine)
        except ImportError:
            self.fail("PromptTemplateEngine class not found. Please create it in prompt_template_engine.py")

    def test_intent_detection_post_engagement(self):
        """RED: Test intent detection for post engagement actions."""
        from prompt_template_engine import PromptTemplateEngine
        engine = PromptTemplateEngine()
        
        # Test cases for post engagement intent
        test_cases = [
            "Like 3 posts about AI",
            "React to posts about machine learning", 
            "Like the latest post by John Doe"
        ]
        
        for prompt in test_cases:
            intent = engine.detect_intent(prompt)
            self.assertEqual(intent, "post_engagement", 
                           f"Expected 'post_engagement' intent for: '{prompt}'")

    def test_intent_detection_comment_post(self):
        """RED: Test intent detection for commenting actions.""" 
        from prompt_template_engine import PromptTemplateEngine
        engine = PromptTemplateEngine()
        
        test_cases = [
            "Comment 'Great insights!' on latest post by Satya Nadella",
            "Add comment to post about AI trends",
            "Reply to the top post in my feed"
        ]
        
        for prompt in test_cases:
            intent = engine.detect_intent(prompt)
            self.assertEqual(intent, "comment_post",
                           f"Expected 'comment_post' intent for: '{prompt}'")

    def test_parameter_extraction_numbers(self):
        """RED: Test extraction of numeric parameters."""
        from prompt_template_engine import PromptTemplateEngine
        engine = PromptTemplateEngine()
        
        test_cases = [
            ("Like 3 posts about AI", {"count": 3}),
            ("Connect with 5 Google employees", {"count": 5}),
            ("Find 10 posts about startups", {"count": 10})
        ]
        
        for prompt, expected_params in test_cases:
            params = engine.extract_parameters(prompt)
            self.assertIn("count", params, f"No 'count' parameter found in: '{prompt}'")
            self.assertEqual(params["count"], expected_params["count"])

    def test_parameter_extraction_keywords(self):
        """RED: Test extraction of keyword/topic parameters."""
        from prompt_template_engine import PromptTemplateEngine
        engine = PromptTemplateEngine()
        
        test_cases = [
            ("Like posts about AI", {"keywords": ["AI"]}),
            ("Find posts about machine learning and startups", {"keywords": ["machine learning", "startups"]}),
            ("Comment on posts about generative AI", {"keywords": ["generative AI"]})
        ]
        
        for prompt, expected_params in test_cases:
            params = engine.extract_parameters(prompt)
            self.assertIn("keywords", params, f"No 'keywords' parameter found in: '{prompt}'")
            self.assertEqual(params["keywords"], expected_params["keywords"])

    def test_template_selection_and_rendering(self):
        """RED: Test template selection and basic rendering."""
        from prompt_template_engine import PromptTemplateEngine
        engine = PromptTemplateEngine()
        
        prompt = "Like 3 posts about AI"
        template = engine.select_template(prompt)
        self.assertIsNotNone(template, "No template selected for post engagement action")
        
        # Test rendering with parameters
        rendered = engine.render_template(template, {"count": 3, "keywords": ["AI"]})
        self.assertIsInstance(rendered, str, "Rendered template should be a string")
        self.assertIn("3", rendered, "Rendered template should contain the count parameter")
        self.assertIn("AI", rendered, "Rendered template should contain the keyword parameter")

    # === CYCLE 1.5: LLM-POWERED TESTS ===
    
    @patch('openai.OpenAI')
    def test_llm_intent_detection_contextual_understanding(self, mock_openai):
        """RED: Test LLM can understand contextual synonyms for intent detection."""
        from prompt_template_engine import PromptTemplateEngine
        
        # Mock LLM response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "post_engagement"
        mock_client.chat.completions.create.return_value = mock_response
        
        engine = PromptTemplateEngine(use_llm=True)
        
        # Test contextual understanding - these should all be detected as post_engagement
        contextual_cases = [
            "Show some love to AI posts",
            "Give a thumbs up to machine learning content", 
            "Appreciate posts about startups",
            "Express approval for recent tech posts"
        ]
        
        for prompt in contextual_cases:
            intent = engine.detect_intent_with_llm(prompt)
            self.assertEqual(intent, "post_engagement",
                           f"LLM failed to detect 'post_engagement' for contextual prompt: '{prompt}'")

    @patch('openai.OpenAI')
    def test_llm_parameter_extraction_complex_language(self, mock_openai):
        """RED: Test LLM can extract parameters from complex natural language."""
        from prompt_template_engine import PromptTemplateEngine
        
        # Mock LLM response for complex parameter extraction
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"count": 5, "keywords": ["artificial intelligence", "machine learning"], "target_person": "Sundar Pichai"}'
        mock_client.chat.completions.create.return_value = mock_response
        
        engine = PromptTemplateEngine(use_llm=True)
        
        prompt = "Please like five posts about artificial intelligence and machine learning from Sundar Pichai's recent activity"
        params = engine.extract_parameters_with_llm(prompt)
        
        self.assertEqual(params["count"], 5)
        self.assertIn("artificial intelligence", params["keywords"])
        self.assertIn("machine learning", params["keywords"])  
        self.assertEqual(params["target_person"], "Sundar Pichai")

    @patch('openai.OpenAI')
    def test_llm_fallback_integration(self, mock_openai):
        """RED: Test graceful fallback to keyword matching when LLM fails."""
        from prompt_template_engine import PromptTemplateEngine
        
        # Mock LLM failure
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        engine = PromptTemplateEngine(use_llm=True)
        
        # Should fallback to keyword matching
        prompt = "Like 3 posts about AI"
        intent = engine.detect_intent(prompt)  # This should use fallback
        self.assertEqual(intent, "post_engagement", "Fallback to keyword matching failed")

    def test_openai_client_initialization(self):
        """RED: Test OpenAI client is properly initialized when use_llm=True."""
        from prompt_template_engine import PromptTemplateEngine
        
        engine = PromptTemplateEngine(use_llm=True)
        self.assertTrue(hasattr(engine, 'openai_client'), "OpenAI client not initialized")
        self.assertIsNotNone(engine.openai_client, "OpenAI client is None")

if __name__ == '__main__':
    unittest.main()
