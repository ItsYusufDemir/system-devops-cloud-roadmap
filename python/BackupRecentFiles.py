"""
Backup Recent Files

✔ Concepts: os module, file paths, conditions
✔ DevOps relevance: Automating backups & deployment packaging

Task:
Create a script that:

Checks a folder

Copies only files modified in the last 24 hours into a backup/ folder


"""

import sys
import os
import time
import shutil

LAST_ACCESS_TIME = 3600 * 24 # SECONDS
BACKUP_PATH = "python/backup"  # ./backup in current dir

counter = 0




def backup(folder_path):

    accessed_files = []

    global counter


    try:


        dir_list = os.listdir(folder_path)

        current_time = time.time()

        for i in dir_list:
            full_path = os.path.join(folder_path, i)

            if (os.path.isdir(full_path)):
                backup(full_path)
                continue

            access_time = os.path.getmtime(full_path)
            
            if (current_time - access_time < LAST_ACCESS_TIME):
                counter += 1
                accessed_files.append(full_path)




        if (len(accessed_files) == 0):
            return

        


        for file_path in accessed_files:
            shutil.copy(file_path, BACKUP_PATH)


          
    except FileNotFoundError:
        print(f"Path {folder_path} does not exist!")
    except NotADirectoryError:
        print(f"Path {folder_path} is not a directory!")
    except PermissionError:
        print(f"Path {folder_path} cannot access to the directory")


try:
    folder_path = sys.argv[1]


    os.makedirs(BACKUP_PATH, exist_ok=True)
    print("Starting backup...")

    backup(folder_path)

    print(f"{counter} files has been modified in the last 24 hours")
    print("Backup completed.")



except Exception as e:
    print("Usage: BackupRecentFiles.py <path-to-folder>",e)
    sys.exit(1)

