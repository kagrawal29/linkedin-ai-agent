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
        # TEMPORARILY DISABLED TO TEST GENERIC ENHANCEMENT
        if False and self.use_templates and self.template_engine:
            try:
                template_enhanced = self._try_template_enhancement(clean_prompt)
                if template_enhanced:
                    return template_enhanced
            except Exception as e:
                print(f"Template enhancement failed: {e}")
                print("Falling back to generic enhancement.")
        
        # Fall back to generic enhancement
        enhanced_prompt = self._enhance_generic(clean_prompt)
        
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
    
    def _enhance_generic(self, prompt: str) -> str:
        """
        Enhance prompt with generic LinkedIn automation guidelines.
        This should create detailed, actionable browser-use instructions.
        """
        # Analyze the prompt for key actions and parameters
        prompt_lower = prompt.lower()
        
        # Extract key information
        actions = []
        if any(word in prompt_lower for word in ['find', 'search', 'look for']):
            actions.append('search')
        if any(word in prompt_lower for word in ['comment', 'reply', 'respond']):
            actions.append('comment')
        if any(word in prompt_lower for word in ['like', 'react']):
            actions.append('like')
        if any(word in prompt_lower for word in ['connect', 'follow']):
            actions.append('connect')
        if any(word in prompt_lower for word in ['post', 'share', 'publish']):
            actions.append('post')
        
        # Extract topics/keywords
        topics = []
        for topic in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'workflow', 'automation', 'startup', 'tech']:
            if topic in prompt_lower:
                topics.append(topic)
        
        # Build detailed execution plan
        base_prompt = f"""You are working on LinkedIn using browser automation. You have specific tasks to complete.

Original Task: {prompt}

DETAILED BROWSER AUTOMATION PLAN:
"""
        
        if 'search' in actions:
            base_prompt += f"""
1. SEARCH PHASE:
   - Navigate to LinkedIn feed or search
   - Use search terms: {', '.join(topics) if topics else 'relevant keywords from prompt'}
   - Filter results for recent, engaging posts
   - Identify 3-5 high-quality posts from the search results
   - Take note of post authors, content, and engagement levels
"""

        if 'comment' in actions:
            # Check if this is a draft-only request
            is_draft_only = any(phrase in prompt_lower for phrase in ["don't post", "dont post", "draft", "don't submit"])
            submit_instruction = "Draft comments in comment boxes but DO NOT SUBMIT yet" if is_draft_only else "Submit well-crafted comments"
            
            base_prompt += f"""
2. RESEARCH PHASE:
   - For each identified post, read the full content carefully
   - Check the author's profile and background
   - Review existing comments to avoid duplication
   - Research the topic mentioned to provide informed insights
   - Formulate thoughtful, value-adding comments (100-200 words each)

3. COMMENT COMPOSITION:
   - Write comments that demonstrate expertise and genuine interest
   - Include specific insights or questions related to the post content
   - Reference your own experience or ask thoughtful follow-up questions
   - Ensure each comment adds unique value to the conversation
   - {submit_instruction}
"""

        if 'like' in actions:
            base_prompt += f"""
4. ENGAGEMENT PHASE:
   - Like posts that align with your interests and expertise
   - Prioritize posts from thought leaders and industry experts  
   - Avoid liking low-quality or controversial content
"""

        base_prompt += f"""
EXECUTION GUIDELINES:
- Work methodically through each phase
- Spend adequate time on research (2-3 minutes per post)
- Ensure all comments are professional and value-adding
- Respect rate limits - take 30-second breaks between actions
- Maintain authentic, human-like interaction patterns
- Double-check all text before submitting

SUCCESS METRICS:
- Find posts that are genuinely relevant and high-quality
- Write comments that could generate meaningful replies
- Demonstrate subject matter expertise through thoughtful insights
- Complete all phases without triggering LinkedIn's spam detection

LinkedIn DOM HINTS:
- Search box: [data-test-id="search-keywords-input"] or input[placeholder*="Search"]
- Like buttons: button[aria-label*="Like"] or button[data-test-id*="like"]
- Comment boxes: div[contenteditable="true"] or textarea[placeholder*="comment"]
- Post content: div[data-test-id="post-content"] or article containers
- Submit buttons: button[type="submit"] or button[aria-label*="Post"] 

Execute this plan step by step, taking time for proper research and thoughtful engagement."""

        return base_prompt
