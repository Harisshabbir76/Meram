import os

files_to_delete = [
    'check_favicon.py',
    'find_favicon.py',
    'find_recent_files.py',
    'inspect_db.py',
]

for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        print(f"Deleted {f}")
