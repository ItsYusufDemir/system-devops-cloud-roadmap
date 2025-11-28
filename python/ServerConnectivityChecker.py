"""
Server Connectivity Checker
Concepts: subprocess module, exit codes, lists.

DevOps Relevance: building "glue code" to run system commands and verifying network connectivity.

Task: Write a script that:

Defines a list of servers (e.g., ["google.com", "github.com", "fake-server.local"]).

Loops through the list and runs the system ping command for each (send only 1 packet).

Checks the exit code (0 = success, non-zero = failure).

Prints [ONLINE] {server} or [OFFLINE] {server} based on the result.

Hint: Use subprocess.run(["ping", "-c", "1", server], capture_output=True) to run the command without cluttering your terminal.

"""

import subprocess
import re

server_list = ["google.com", "yok.gov.tr", "instagram.com", "facebook.com"]
#server_list = ["google.com"]


for server in server_list:
    command = ["ping", "-c", "1"]
    command.append(server)
    answer = subprocess.run(command, capture_output=True)

    if answer.returncode == 0:

        output = answer.stdout.decode("utf-8")
        latency = re.search(r"time=([\d.]+)", output).group(1)

        print(f"[ONLINE] {server} {latency} ms")
    else:
        print(f"[OFFLINE] {server}")