import threading
import time
import os
import shutil
from random import sample
import json

def clearfile(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            clearfile(file_path)
        elif file.split('.')[-1] != 'jar':
            os.system(f"rm {file_path}")
            
clearfile("../static/workplace/users")