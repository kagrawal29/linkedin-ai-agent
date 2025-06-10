# File: executor.py
#
# Purpose: This file is the agent's 'hands'.
#
# After all the thinking, researching, and writing is done, this file is
# responsible for taking the final action and interacting directly with the
# LinkedIn website.
#
# How it works:
# 1.  The 'agent.py' tells it what to do, for example, "like this post" or
#     "post this comment".
# 2.  It uses its connection to the web browser (managed by 'harvester.py') to
#     find the exact buttons and text boxes on the LinkedIn page.
# 3.  It performs the action, such as:
#     - Clicking the 'Like' button.
#     - Typing the comment into the comment box and clicking 'Post'.
#     - Sending a connection request or a direct message.
# 4.  It's also built to be resilient. If it can't find a button (for example,
#     if the page is loading slowly), it will try a few more times before giving up.
# 5.  It reports back to 'agent.py' whether the action was successful.
