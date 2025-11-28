import subprocess


a = subprocess.run(["ping", "-c", "1", "google.com"], capture_output=True)


print(a)