import subprocess
import pandas as pd
images = subprocess.run(['docker', 'images']).stdout
print(images)
print(type(images))

for i in images:
    print(i)
