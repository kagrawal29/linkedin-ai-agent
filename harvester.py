# File: harvester.py
#
# Purpose: This file is the agent's 'web browser' and 'data collector'.
#
# It is responsible for opening a web browser, navigating to LinkedIn, and
# gathering all the posts from the feed, just like a person would when scrolling.
#
# How it works:
# 1.  The 'agent.py' tells it to start its work.
# 2.  It launches a browser (like Chrome) and makes sure it's logged into your
#     LinkedIn account securely, without needing to ask for your password.
# 3.  It then begins to scroll down the LinkedIn feed automatically.
# 4.  As it scrolls, it carefully 'reads' each post and extracts the important
#     information: who wrote it, what the post says, how many likes it has, etc.
# 5.  It collects a list of all these posts and hands them back to the 'agent.py'
#     for the next step in the process, which is filtering.
