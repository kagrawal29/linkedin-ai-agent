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

if __name__ == '__main__':
    unittest.main()
