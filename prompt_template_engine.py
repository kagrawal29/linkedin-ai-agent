import re
import json
import os
from typing import Dict, List, Optional
from functools import lru_cache

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class PromptTemplateEngine:
    """
    A class to manage and render prompt templates for LinkedIn actions.
    Supports both keyword-based and LLM-powered intent detection with fallback.
    """
    
    # Intent constants
    INTENT_POST_ENGAGEMENT = "post_engagement"
    INTENT_COMMENT_POST = "comment_post"
    INTENT_CONNECT_FOLLOW = "connect_follow"
    INTENT_MESSAGE = "message"
    INTENT_SEARCH_CONTENT = "search_content"
    INTENT_VISIT_PROFILE = "visit_profile"
    INTENT_CREATE_POST = "create_post"
    INTENT_DATA_EXTRACT = "data_extract"
    INTENT_FEED_COLLECTION = "feed_collection"
    INTENT_UNKNOWN = "unknown"
    
    # Intent keywords mapping
    INTENT_KEYWORDS = {
        INTENT_POST_ENGAGEMENT: ['like', 'react', 'appreciate', 'love', 'thumbs up', 'approval'],
        INTENT_COMMENT_POST: ['comment', 'reply', 'respond', 'add thoughts'],
        INTENT_CONNECT_FOLLOW: ['connect', 'follow', 'add'],
        INTENT_MESSAGE: ['message', 'send', 'dm', 'inmail'],
        INTENT_SEARCH_CONTENT: ['search', 'find', 'discover', 'look for'],
        INTENT_VISIT_PROFILE: ['profile', 'visit', 'open', 'view'],
        INTENT_CREATE_POST: ['post', 'create', 'publish', 'share', 'write'],
        INTENT_DATA_EXTRACT: ['extract', 'export', 'data', 'gather', 'collect data'],
        INTENT_FEED_COLLECTION: ['scroll', 'feed', 'collect posts', 'browse']
    }
    
    # LLM Configuration
    DEFAULT_MODEL = "gpt-4o-mini"
    INTENT_CLASSIFICATION_PROMPT = """
Classify this LinkedIn automation request into one of these intents:

- post_engagement: liking, reacting to posts, showing appreciation
- comment_post: commenting, replying to posts, adding thoughts
- create_post: writing, publishing, sharing new content
- search_content: finding, discovering posts/profiles/content
- connect_follow: connecting with people, following users
- message: sending DMs, InMail, private messages
- visit_profile: viewing, opening someone's profile
- data_extract: exporting, collecting, gathering data
- feed_collection: scrolling, browsing feed, collecting posts

User request: "{prompt}"

Respond with just the intent name (e.g., "post_engagement").
"""
    
    PARAMETER_EXTRACTION_PROMPT = """
Extract parameters from this LinkedIn automation request. Return a JSON object with these possible fields:

- count: numeric value (how many items to process)
- keywords: array of topics/keywords to search for
- target_person: specific person's name mentioned
- target_company: specific company mentioned
- timeframe: time period mentioned (e.g., "this week", "recent")
- content_type: type of content (posts, articles, etc.)

Only include fields that are explicitly mentioned or can be clearly inferred.

User request: "{prompt}"

Respond with valid JSON only.
"""
    
    def __init__(self, use_llm: bool = False, openai_api_key: Optional[str] = None, model: str = None):
        self.use_llm = use_llm
        self.model = model or self.DEFAULT_MODEL
        self.openai_client = None
        
        if self.use_llm:
            self._initialize_openai_client(openai_api_key)
    
    def _initialize_openai_client(self, api_key: Optional[str] = None) -> None:
        """Initialize OpenAI client with proper error handling."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")
        
        resolved_api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not resolved_api_key:
            raise ValueError("OpenAI API key required when use_llm=True. Set OPENAI_API_KEY environment variable.")
        
        self.openai_client = openai.OpenAI(api_key=resolved_api_key)
    
    def detect_intent(self, prompt: str) -> str:
        """Detect intent using LLM if enabled, otherwise fall back to keyword matching."""
        if self.use_llm and self.openai_client:
            try:
                return self.detect_intent_with_llm(prompt)
            except Exception as e:
                print(f"LLM intent detection failed: {e}. Falling back to keyword matching.")
                return self._detect_intent_keywords(prompt)
        else:
            return self._detect_intent_keywords(prompt)
    
    def _detect_intent_keywords(self, prompt: str) -> str:
        """Original keyword-based intent detection with enhanced keyword matching."""
        prompt_lower = prompt.lower()
        
        # Score-based matching for better accuracy
        intent_scores = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            # Return intent with highest score
            return max(intent_scores, key=intent_scores.get)
        
        return self.INTENT_UNKNOWN
    
    @lru_cache(maxsize=128)
    def detect_intent_with_llm(self, prompt: str) -> str:
        """Use GPT-4o Mini to detect intent from natural language with caching."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Set use_llm=True in constructor.")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a LinkedIn automation intent classifier. Respond only with the intent name."},
                    {"role": "user", "content": self.INTENT_CLASSIFICATION_PROMPT.format(prompt=prompt)}
                ],
                max_tokens=20,
                temperature=0.1
            )
            
            intent = response.choices[0].message.content.strip()
            
            # Validate that returned intent is one of our known intents
            all_intents = [getattr(self, attr) for attr in dir(self) if attr.startswith('INTENT_') and not attr.endswith('_KEYWORDS')]
            if intent in all_intents:
                return intent
            else:
                # Fallback if LLM returns unknown intent
                return self._detect_intent_keywords(prompt)
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise
    
    def extract_parameters(self, prompt: str) -> Dict:
        """Extract parameters using LLM if enabled, otherwise use regex."""
        if self.use_llm and self.openai_client:
            try:
                return self.extract_parameters_with_llm(prompt)
            except Exception as e:
                print(f"LLM parameter extraction failed: {e}. Falling back to regex.")
                return self._extract_parameters_regex(prompt)
        else:
            return self._extract_parameters_regex(prompt)
    
    def _extract_parameters_regex(self, prompt: str) -> Dict:
        """Enhanced regex-based parameter extraction."""
        params = {}
        
        # Extract numeric count with better patterns
        count_patterns = [
            r'\b(\d+)\s+posts?\b',  # "3 posts"
            r'\b(\d+)\s+(?:times?|items?)\b',  # "5 times"
            r'\bfind\s+(\d+)\b',  # "find 10"
            r'\b(\d+)\b'  # any number (fallback)
        ]
        
        for pattern in count_patterns:
            count_match = re.search(pattern, prompt, re.IGNORECASE)
            if count_match:
                params["count"] = int(count_match.group(1))
                break
        
        # Extract keywords with improved patterns
        keywords = self._extract_keywords(prompt)
        if keywords:
            params["keywords"] = keywords
        
        # Extract person names (basic pattern)
        person_match = re.search(r'(?:by|from)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', prompt)
        if person_match:
            params["target_person"] = person_match.group(1)
        
        return params
    
    @lru_cache(maxsize=64)
    def extract_parameters_with_llm(self, prompt: str) -> Dict:
        """Use GPT-4o Mini to extract parameters from complex natural language with caching."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Set use_llm=True in constructor.")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a parameter extraction assistant. Respond only with valid JSON."},
                    {"role": "user", "content": self.PARAMETER_EXTRACTION_PROMPT.format(prompt=prompt)}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            response_content = response.choices[0].message.content.strip()
            return json.loads(response_content)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}. Content: {response_content}")
            return self._extract_parameters_regex(prompt)
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise
    
    def _extract_keywords(self, prompt: str) -> List[str]:
        """Enhanced keyword extraction with multiple patterns."""
        patterns = [
            r'about\s+(.+?)(?:\s+(?:with|by|from|in)|\s*$)',  # "about AI"
            r'on\s+(.+?)(?:\s+(?:with|by|from|in)|\s*$)',     # "on machine learning"
            r'related to\s+(.+?)(?:\s+(?:with|by|from|in)|\s*$)',  # "related to startups"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                keyword_text = match.group(1).strip()
                # Handle multiple keywords separated by "and"
                if " and " in keyword_text:
                    return [k.strip() for k in keyword_text.split(" and ")]
                else:
                    return [keyword_text]
        return []
    
    def select_template(self, prompt: str) -> str:
        """Select appropriate template based on prompt intent."""
        intent = self.detect_intent(prompt)
        return f"{intent}_template"
    
    def render_template(self, template: str, parameters: Dict) -> str:
        """Render template with given parameters."""
        template_renderers = {
            f"{self.INTENT_POST_ENGAGEMENT}_template": self._render_post_engagement_template,
            f"{self.INTENT_COMMENT_POST}_template": self._render_comment_post_template,
        }
        
        renderer = template_renderers.get(template)
        if renderer:
            return renderer(parameters)
        else:
            return "1. Navigate to LinkedIn\n2. Perform the requested action"
    
    def _render_post_engagement_template(self, parameters: Dict) -> str:
        """Render enhanced post engagement template."""
        count = parameters.get("count", 1)
        keywords = parameters.get("keywords", ["content"])
        target_person = parameters.get("target_person")
        
        keyword_text = " and ".join(keywords)
        steps = [
            "1. Navigate to LinkedIn feed",
            f"2. Search for {count} posts about {keyword_text}"
        ]
        
        if target_person:
            steps[1] += f" from {target_person}"
        
        steps.extend([
            "3. Click the like button on each relevant post",
            "4. Verify the like was successful",
            "5. Wait briefly between actions to avoid rate limiting"
        ])
        
        return "\n".join(steps)
    
    def _render_comment_post_template(self, parameters: Dict) -> str:
        """Render enhanced comment post template."""
        keywords = parameters.get("keywords", ["content"])
        comment_text = parameters.get("comment_text", "Great insights!")
        
        keyword_text = " and ".join(keywords)
        return f"""1. Navigate to LinkedIn feed
2. Find posts about {keyword_text}
3. Click the comment button on the target post
4. Type comment: "{comment_text}"
5. Review comment for appropriateness
6. Submit the comment
7. Verify comment was posted successfully"""
