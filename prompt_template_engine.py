import re

class PromptTemplateEngine:
    """
    A class to manage and render prompt templates for LinkedIn actions.
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
        INTENT_POST_ENGAGEMENT: ['like', 'react'],
        INTENT_COMMENT_POST: ['comment', 'reply'],
        INTENT_CONNECT_FOLLOW: ['connect', 'follow'],
        INTENT_MESSAGE: ['message', 'send'],
        INTENT_SEARCH_CONTENT: ['search', 'find'],
        INTENT_VISIT_PROFILE: ['profile', 'visit', 'open'],
        INTENT_CREATE_POST: ['post', 'create', 'publish'],
        INTENT_DATA_EXTRACT: ['extract', 'export', 'data'],
        INTENT_FEED_COLLECTION: ['scroll', 'feed', 'collect']
    }
    
    def __init__(self):
        pass
    
    def detect_intent(self, prompt):
        """Detect the intent from natural language prompt."""
        prompt_lower = prompt.lower()
        
        # Check each intent against its keywords
        for intent, keywords in self.INTENT_KEYWORDS.items():
            if any(word in prompt_lower for word in keywords):
                return intent
        
        return self.INTENT_UNKNOWN
    
    def extract_parameters(self, prompt):
        """Extract parameters from natural language prompt."""
        params = {}
        
        # Extract numeric count
        count_match = re.search(r'\b(\d+)\b', prompt)
        if count_match:
            params["count"] = int(count_match.group(1))
        
        # Extract keywords after "about"
        keywords = self._extract_keywords(prompt)
        if keywords:
            params["keywords"] = keywords
        
        return params
    
    def _extract_keywords(self, prompt):
        """Helper method to extract keywords from prompt."""
        about_match = re.search(r'about\s+(.+?)(?:\s+(?:with|by|from|in)|\s*$)', prompt, re.IGNORECASE)
        if about_match:
            keyword_text = about_match.group(1).strip()
            # Split on "and" to handle multiple keywords
            if " and " in keyword_text:
                return [k.strip() for k in keyword_text.split(" and ")]
            else:
                return [keyword_text]
        return []
    
    def select_template(self, prompt):
        """Select appropriate template based on prompt intent."""
        intent = self.detect_intent(prompt)
        return f"{intent}_template"
    
    def render_template(self, template, parameters):
        """Render template with given parameters."""
        if template == f"{self.INTENT_POST_ENGAGEMENT}_template":
            return self._render_post_engagement_template(parameters)
        elif template == f"{self.INTENT_COMMENT_POST}_template":
            return self._render_comment_post_template(parameters)
        else:
            return "1. Navigate to LinkedIn\n2. Perform the requested action"
    
    def _render_post_engagement_template(self, parameters):
        """Render post engagement template."""
        count = parameters.get("count", 1)
        keywords = parameters.get("keywords", ["content"])
        keyword_text = " and ".join(keywords)
        return f"1. Navigate to LinkedIn feed\n2. Find {count} posts about {keyword_text}\n3. Click the like button on each post\n4. Verify the like was successful"
    
    def _render_comment_post_template(self, parameters):
        """Render comment post template."""
        keywords = parameters.get("keywords", ["content"])
        keyword_text = " and ".join(keywords)
        return f"1. Navigate to LinkedIn feed\n2. Find posts about {keyword_text}\n3. Click comment button\n4. Type comment text\n5. Submit comment"
