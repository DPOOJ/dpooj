import threading
import time
import os
import shutil
from random import sample
import json
import sys

sys.argv.append(3)

i = 0
while True:
    print(i)
    i += 1
    time.sleep(1)
    