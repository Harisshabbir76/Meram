import os
import time

now = time.time()
two_days_ago = now - 2 * 24 * 3600

for root, dirs, files in os.walk('.'):
    for f in files:
        path = os.path.join(root, f)
        try:
            mtime = os.path.getmtime(path)
            if mtime > two_days_ago:
                print(f"{path} - modified: {time.ctime(mtime)}")
        except Exception:
            pass
