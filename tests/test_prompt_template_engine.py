import unittest
from unittest.mock import patch

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

if __name__ == '__main__':
    unittest.main()
