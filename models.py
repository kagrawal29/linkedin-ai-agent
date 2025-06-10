from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class FetchedPost(BaseModel):
    post_id: str = Field(..., description="Unique identifier for the post, if available (e.g., from its URL or a data attribute).")
    post_url: HttpUrl = Field(..., description="Direct URL to the LinkedIn post.")
    author_name: str = Field(..., description="Name of the post's author.")
    author_url: Optional[HttpUrl] = Field(None, description="URL to the author's LinkedIn profile, if available.")
    author_headline: Optional[str] = Field(None, description="Author's headline or short bio, if available.")
    content_text: str = Field(..., description="The main text content of the post.")
    posted_timestamp_str: Optional[str] = Field(None, description="Raw string representation of when the post was made (e.g., '2h', '1d', 'July 10').")
    likes_count: Optional[int] = Field(None, description="Number of likes or reactions.")
    comments_count: Optional[int] = Field(None, description="Number of comments.")
    reposts_count: Optional[int] = Field(None, description="Number of reposts/shares.")
    views_count: Optional[int] = Field(None, description="Number of views, if available (especially for videos or articles).")

    class Config:
        # Pydantic V2: json_schema_extra can be used for examples in OpenAPI docs
        # For Pydantic V1, schema_extra was used.
        # If we generate OpenAPI schema later, this can be useful.
        # Example for Pydantic v2:
        # json_schema_extra = {
        #     "example": {
        #         "post_id": "urn:li:activity:1234567890123456789",
        #         "post_url": "https://www.linkedin.com/feed/update/urn:li:activity:1234567890123456789/",
        #         "author_name": "Jane Doe",
        #         "author_url": "https://www.linkedin.com/in/janedoe/",
        #         "author_headline": "AI Enthusiast | Building the Future",
        #         "content_text": "Excited to share my latest thoughts on AI in fintech! It's revolutionizing the industry.",
        #         "posted_timestamp_str": "5h",
        #         "likes_count": 125,
        #         "comments_count": 15,
        #         "reposts_count": 7,
        #         "views_count": 1500
        #     }
        # }
        pass
