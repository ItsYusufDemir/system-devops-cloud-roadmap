"""
Log File Analyzer

✔ Concepts: File handling, loops, string operations
✔ DevOps relevance: Logs are everywhere — monitoring, troubleshooting, automation

Task:
Write a script that:

Reads a .log file

Counts how many times the word "error" appears

Prints the total count

🧠 Why: This helps you automate server health monitoring.
"""

import sys

try:
    log_file = sys.argv[1] # argv[0] is this python file path/name, so our real argv is in index 1

    try:
        file = open(log_file)

        row_number = 1
        line = file.readline()
        while line:
            line = line.lower()
            condition = line.find("error")

            if (condition != -1):
                print(f"\033[1;34m{row_number}:{condition}\033[0m || \033[1;92m{line}\033[0m")
                

            row_number += 1
            line = file.readline()


    except:
        print("Log file couldn't opened")

except: 
    print("Usage: python3 LogFileAnalyzer.py <log-file>")








