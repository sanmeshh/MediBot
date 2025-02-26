import os
from pathlib import Path 
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s:')

#modular approach

list_files=[
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py"
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trails.ipynb"
]

for filepath in list_files:
    filepath=Path(filepath)#generalized filepath for each os(windows,mac,linux,etc)
    filedir,filename=os.path.split(filepath)

    if filedir!="":#if not empty
        os.makedirs(filedir,exist_ok=True)#making file directory
        logging.info(f"Creating directory: {filepath} for the file :{filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):#if file is empty,we create the file:
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")


