# File: logger.py
#
# Purpose: This file is the agent's 'official record-keeper' or 'diarist'.
#
# Its sole responsibility is to write down every single action the agent takes,
# creating a complete and transparent log. This is crucial for reviewing what
# the agent has done, debugging any issues, and ensuring it's behaving as expected.
#
# How it works:
# 1.  Throughout the entire process, the 'agent.py' tells this file what's happening.
# 2.  For every event—from starting up, to harvesting a post, to posting a comment—
#     this file writes a new line in a log file.
# 3.  Each log entry is structured and contains key details, such as:
#     - A timestamp of when the action happened.
#     - The action that was performed (e.g., 'comment', 'like').
#     - The URL of the post that was interacted with.
#     - The exact text of the comment that was posted.
#     - Any research links that were used.
# 4.  This creates a permanent, tamper-proof record that can be easily searched
#     and reviewed later.
