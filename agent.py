# File: agent.py
#
# Purpose: This is the master controller for the entire LinkedIn AI Agent.
#
# Think of this file as the "brain" of the operation. It's responsible for
# coordinating all the other specialized files to get the job done.
#
# How it works:
# 1.  It starts when you run the program.
# 2.  It takes your instruction, like "comment on 3 posts about AI".
# 3.  It tells the 'interpreter.py' file to make sense of your instruction.
# 4.  Once it understands what to do, it tells the 'harvester.py' to go to LinkedIn and find relevant posts.
# 5.  It then passes these posts to the 'filter_engine.py' to narrow them down to the very best ones.
# 6.  For each of the best posts, it asks the 'researcher.py' to gather more information to make the comment smart.
# 7.  It gives this research to the 'commenter.py', which writes a thoughtful, human-like comment.
# 8.  Finally, it tells the 'executor.py' to actually post the comment on LinkedIn.
# 9.  Throughout this whole process, it instructs the 'logger.py' to keep a detailed diary of every action taken.
