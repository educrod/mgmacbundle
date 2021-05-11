#!/usr/bin/env python3
import subprocess
import shlex
import shutil
import os
import logging

logging.basicConfig(level=logging.INFO)

logging.info("backuping old versions")

def get_project_name():
    with open("app.manifest", 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.lstrip().startswith("<assemblyIdentity"):
            project_name = line.partition("name=\"")[2].rstrip('\n\"/>').title()
            print(project_name)
            

if os.path.isdir("bin/Release/osx-64/"):
    print("lele")
else:
    print("lala")

publish_command = shlex.split("dotnet publish -c Release -r osx-x64 /p:PublishReadyToRun=false /p:TieredCompilation=false --self-contained")

try:
    subprocess.run(publish_command,check=True, capture_output=True)
except subprocess.CalledProcessError as err:
    logging.error(str(err.output))


get_project_name()