# Here is a very simple, "no-jargon" explanation of what each file does. You can copy this into a separate document to use as a script for your presentation or as a reference for your report.

# 1. master.py (The Boss)
# This is the "brain" of the whole operation. It sits in the middle and manages everything.

# The Job: It reads your text file (input.txt) and breaks it into pieces.

# The Server: It opens a "communication line" (Port 6000) so that workers can call in and ask for work.

# The Collector: When workers finish their task, the Boss takes their results, groups the same words together, and does the final math.

# The Website: It also runs the dashboard you see in your browser so you can watch the progress live.

# 2. worker.py (The Laborer)
# This file represents a single worker. You can run many of these at the same time.

# The Connection: It calls the Boss and says, "I'm ready to work".

# The Map Phase: It takes one line of text, breaks it into individual words, and puts a "1" next to each word.

# The Safety: It is designed to be tough. If the Boss stops talking, the worker just shuts down quietly instead of causing a big error.

# 3. mapreduce_helper.py (The Instruction Manual)
# This is a small file that tells the workers and the boss exactly how to handle the words.

# The Mapper: It tells the workers how to clean the text (like making it lowercase) and how to split the words.

# The Reducer: It tells the boss how to add up all those "1s" to get the final total for each word.

# 4. launch_army.py (The Starter Button)
# Instead of you manually clicking "Run" on 10 different worker files, this script does it for you.

# The Army: It tells the computer to start 10 workers all at once in the background.

# The Speed: This is what makes the system "parallel"—because 10 workers are processing 10 different lines of text at the exact same time.

# 5. templates/index.html (The Dashboard)
# This is the visual part that you actually look at.

# The UI: It’s a webpage that displays "Unique Words" and "Tasks Completed".

# The Live Update: It has a small timer inside that "pokes" the Boss every 1 second to ask, "Any new results?" and then updates the screen immediately.

# Summary of the Workflow (For your presentation)
# Start the Boss (master.py).

# Open the Dashboard (Go to http://127.0.0.1:5000 in Chrome).

# Deploy the Army (launch_army.py).

# Watch the magic: The workers take the work, the Boss collects it, and the Dashboard shows the results.