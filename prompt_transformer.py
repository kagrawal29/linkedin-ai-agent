"""
PromptTransformer module for enhancing user prompts with LinkedIn context and safety validation.

This module replaces the complex PromptInterpreter with a lightweight enhancement approach
that prepares natural language prompts for direct use with browser-use Agent.
"""

from typing import Optional
import re

# Try to import PromptTemplateEngine for advanced template-based enhancement
try:
    from prompt_template_engine import PromptTemplateEngine
    TEMPLATE_ENGINE_AVAILABLE = True
except ImportError:
    TEMPLATE_ENGINE_AVAILABLE = False


class PromptTransformer:
    """
    Lightweight prompt enhancement for LinkedIn automation.
    
    Replaces the complex PromptInterpreter by focusing on prompt enhancement
    rather than structured command parsing. Optimizes prompts for browser-use
    Agent while ensuring professional conduct and safety.
    
    Now supports template-based enhancement via PromptTemplateEngine integration.
    """
    
    def __init__(self, use_templates: bool = False, use_llm: bool = False):
        """
        Initialize PromptTransformer with safety guidelines and context templates.
        
        Args:
            use_templates: Enable advanced template-based enhancement via PromptTemplateEngine
            use_llm: Enable LLM-powered intent detection and parameter extraction (requires use_templates=True)
        """
        self._safety_guidelines = [
            "Maintain professional and respectful tone in all interactions",
            "Ensure all actions are constructive and thoughtful", 
            "Follow LinkedIn's community standards and best practices",
            "Be considerate and appropriate in all engagements",
            "Avoid spam-like behavior or excessive automated actions",
            "Respect others' time and privacy"
        ]
        
        self._linkedin_context = (
            "You are working on LinkedIn, the professional networking platform where "
            "people connect for career opportunities, industry insights, and business relationships."
        )
        
        # Initialize template engine if requested and available
        self.use_templates = use_templates
        self.template_engine = None
        
        if use_templates:
            if not TEMPLATE_ENGINE_AVAILABLE:
                print("Warning: PromptTemplateEngine not available. Falling back to generic enhancement.")
                self.use_templates = False
            else:
                try:
                    self.template_engine = PromptTemplateEngine(use_llm=use_llm)
                except Exception as e:
                    print(f"Warning: Failed to initialize PromptTemplateEngine: {e}")
                    print("Falling back to generic enhancement.")
                    self.use_templates = False
                    self.template_engine = None
    
    def enhance_prompt(self, user_prompt: Optional[str]) -> str:
        """
        Enhance user prompt with LinkedIn context and safety guidelines.
        
        Transforms raw user prompts into optimized instructions for browser-use Agent
        by adding professional context, safety validation, and task clarification.
        
        If template engine is enabled, will attempt to detect LinkedIn action templates
        and render detailed step-by-step instructions. Falls back to generic enhancement
        if no template matches or template engine fails.
        
        Args:
            user_prompt: Raw user input prompt
            
        Returns:
            Enhanced prompt optimized for browser-use Agent execution
            
        Raises:
            ValueError: If prompt is empty or None
        """
        # Validate input
        if not user_prompt or not user_prompt.strip():
            raise ValueError("Empty prompt not allowed")
        
        # Clean and prepare the input
        clean_prompt = self._clean_prompt(user_prompt.strip())
        
        # Try template-based enhancement first if enabled
        if self.use_templates and self.template_engine:
            try:
                template_enhanced = self._try_template_enhancement(clean_prompt)
                if template_enhanced:
                    return template_enhanced
            except Exception as e:
                print(f"Template enhancement failed: {e}")
                print("Falling back to generic enhancement.")
        
        # Fall back to generic enhancement
        enhanced_prompt = self._build_enhanced_prompt(clean_prompt)
        
        return enhanced_prompt
    
    def _try_template_enhancement(self, clean_prompt: str) -> Optional[str]:
        """
        Attempt template-based enhancement using PromptTemplateEngine.
        
        Args:
            clean_prompt: Cleaned user prompt
            
        Returns:
            Template-enhanced prompt if successful, None if no template matches
        """
        if not self.template_engine:
            return None
        
        try:
            # Detect intent using template engine
            intent = self.template_engine.detect_intent(clean_prompt)
            
            if intent == "unknown":
                # No template matches, use generic enhancement
                return None
            
            # Extract parameters for the detected intent
            parameters = self.template_engine.extract_parameters(clean_prompt)
            
            # Render template with extracted parameters
            template_content = self.template_engine.render_template(intent, parameters)
            
            # Build enhanced prompt with template content and safety guidelines
            enhanced_sections = [
                self._linkedin_context,
                "",
                f"Task: {clean_prompt}",
                "",
                "Detailed execution plan:",
                template_content,
                "",
                "Important guidelines:",
            ]
            
            # Add safety guidelines
            for guideline in self._safety_guidelines:
                enhanced_sections.append(f"- {guideline}")
            
            enhanced_sections.extend([
                "",
                "Please execute this LinkedIn automation task while adhering to these professional standards."
            ])
            
            return "\n".join(enhanced_sections)
            
        except Exception as e:
            print(f"Template enhancement error: {e}")
            return None
    
    def _clean_prompt(self, prompt: str) -> str:
        """Clean and normalize the input prompt."""
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', prompt)
        # Ensure proper capitalization for first word
        if cleaned and not cleaned[0].isupper():
            cleaned = cleaned[0].upper() + cleaned[1:]
        return cleaned
    
    def _build_enhanced_prompt(self, clean_prompt: str) -> str:
        """Build the enhanced prompt with LinkedIn context and guidelines."""
        # Create structured enhanced prompt
        enhanced_sections = [
            self._linkedin_context,
            "",  # Empty line for readability
            f"Task: {clean_prompt}",
            "",  # Empty line for readability
            "Important guidelines:",
        ]
        
        # Add safety guidelines as bullet points
        for guideline in self._safety_guidelines:
            enhanced_sections.append(f"- {guideline}")
        
        enhanced_sections.extend([
            "",  # Empty line for readability
            "Please execute this task on LinkedIn while adhering to these professional standards."
        ])
        
        return "\n".join(enhanced_sections)
