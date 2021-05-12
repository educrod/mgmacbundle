#!/usr/bin/env python3
import subprocess
import shlex
import os
import datetime
import logging

logging.basicConfig(level=logging.INFO)

def get_project_name():
    with open("app.manifest", 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.lstrip().startswith("<assemblyIdentity"):
            project_name = line.partition("name=\"")[2].rstrip('\n\"/>').title()
            
    return project_name
            
def backup_old_builds(build_directory):
    app_directory = "{}/{}.app".format(build_directory, get_project_name())
    if os.path.isdir(app_directory):
        os.rename(app_directory, "{}.{}".format(app_directory, datetime.datetime.now().timestamp()))
 
def create_directotory_tree(build_directory):
    if not os.path.isdir(build_directory):
        os.mkdir(build_directory)

def build_app():
    publish_command = shlex.split("dotnet publish -c Release -r osx-x64 /p:PublishReadyToRun=false /p:TieredCompilation=false --self-contained")

    try:
        subprocess.run(publish_command,check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        logging.error(str(err.output))

def main():
    build_directory = "bin/Release/osx-64/"
    create_directotory_tree(build_directory)

if __name__ == "__main__":    
    main()