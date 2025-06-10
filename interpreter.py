# File: interpreter.py
#
# Purpose: This file acts as the agent's 'translator'.
#
# Its main job is to take a simple English command from you (the user) and
# translate it into a detailed, structured set of instructions that the agent
# can understand and follow precisely.
#
# How it works:
# 1.  The 'agent.py' gives it a command, like "Engage with top 3 AI posts today".
# 2.  It uses an AI (like GPT-4) to break down this sentence into its key parts:
#     - Topic: "AI"
#     - Number of posts: 3
#     - Type of engagement: probably 'comment' and 'like'.
# 3.  It packages these details into a neat, organized format (a JSON command).
# 4.  If the original command is unclear (e.g., "Find some posts"), this file is also
#     smart enough to create a question to ask for more details, like "How many posts
#     should I look for?".
# 5.  It then hands these structured instructions back to 'agent.py' to continue the process.
