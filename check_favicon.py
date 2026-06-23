import os

paths = [
    'main/static/main/images/favicon.png',
    'main/static/main/images/Favicon.png',
    'main/static/main/images/favicon.PNG',
    'main/static/main/images/Favicon-04.png',
]

for p in paths:
    print(f"{p}: {os.path.exists(p)}")
