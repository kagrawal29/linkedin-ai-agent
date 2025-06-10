# File: researcher.py
#
# Purpose: This file is the agent's 'research assistant'.
#
# Its job is to take a single, interesting post and gather more context and
# information about it. This ensures that the agent's comments are not just
# generic, but are deep, insightful, and well-informed.
#
# How it works:
# 1.  For a single post that has passed the filter, the 'agent.py' asks this
#     file to do some research.
# 2.  First, it reads the post and creates a short, 80-word summary to understand
#     the main idea.
# 3.  Then, it can use other tools to expand its knowledge, such as:
#     - Searching on DuckDuckGo for related news or articles.
#     - Looking up key terms on Wikipedia.
#     - Finding academic papers on ArXiv if the topic is technical.
# 4.  It bundles all this information—the original post, the summary, and any
#     external articles—into a 'Research Bundle'.
# 5.  It hands this complete bundle back to 'agent.py', ready to be used for
#     writing a comment.
