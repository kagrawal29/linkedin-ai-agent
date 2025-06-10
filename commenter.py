# File: commenter.py
#
# Purpose: This file is the agent's 'voice' or 'writer'.
#
# It takes all the rich information gathered by the 'researcher.py' and uses
# it to compose a high-quality, human-like comment. It pays close attention
# to the agent's personality defined in 'config/persona.md'.
#
# How it works:
# 1.  The 'agent.py' gives it the 'Research Bundle' for a specific post.
# 2.  It reads the agent's persona from 'config/persona.md' to understand the
#     desired tone and style (e.g., analytical, curious, uses analogies).
# 3.  It analyzes the tone of the original post to ensure the comment is a good fit
#     for the conversation.
# 4.  Using all this context, it asks an AI (like GPT-4) to draft a comment that is:
#     - Insightful and adds value.
#     - Reflects the agent's unique persona.
#     - Is appropriate for the context of the original post.
# 5.  It returns the final, polished comment as a piece of text to 'agent.py',
#     ready to be posted.
