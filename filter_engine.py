# File: filter_engine.py
#
# Purpose: This file acts as the agent's 'quality control specialist'.
#
# After the 'harvester.py' gathers a large number of posts, this file's job
# is to sift through them and keep only the ones that are most relevant and
# valuable, based on your preferences.
#
# How it works:
# 1.  The 'agent.py' gives it the full list of posts collected by the harvester.
# 2.  It reads a set of rules from the 'config/filters.yaml' file. These are
#     your personal preferences, such as:
#     - Only show posts with certain keywords (e.g., "AI", "strategy").
#     - Only show posts with more than 20 likes.
#     - Ignore posts that are videos or ads.
# 3.  It checks every post against these rules.
# 4.  It creates a new, shorter list containing only the posts that passed the quality check.
# 5.  It hands this high-quality list back to 'agent.py' for the next step: research.
