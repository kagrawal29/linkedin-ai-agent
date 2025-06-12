"""
PromptTransformer module for enhancing user prompts with LinkedIn context and safety validation.

This module replaces the complex PromptInterpreter with a lightweight enhancement approach
that prepares natural language prompts for direct use with browser-use Agent.
"""

from typing import Optional
import re


class PromptTransformer:
    """
    Lightweight prompt enhancement for LinkedIn automation.
    
    Replaces the complex PromptInterpreter by focusing on prompt enhancement
    rather than structured command parsing. Optimizes prompts for browser-use
    Agent while ensuring professional conduct and safety.
    """
    
    def __init__(self):
        """Initialize PromptTransformer with safety guidelines and context templates."""
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
    
    def enhance_prompt(self, user_prompt: Optional[str]) -> str:
        """
        Enhance user prompt with LinkedIn context and safety guidelines.
        
        Transforms raw user prompts into optimized instructions for browser-use Agent
        by adding professional context, safety validation, and task clarification.
        
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
        
        # Build enhanced prompt with structured sections
        enhanced_prompt = self._build_enhanced_prompt(clean_prompt)
        
        return enhanced_prompt
    
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
