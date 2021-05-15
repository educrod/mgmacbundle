#!/usr/bin/env python3
import subprocess
import shlex
from shutil import copytree, ignore_patterns
from string import Template
import os
import platform
import datetime
import logging

logging.basicConfig(level=logging.INFO)

def get_project_name():
    with open("app.manifest", 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.lstrip().startswith("<assemblyIdentity"):
            #project_name = line.partition("name=\"")[2].rstrip('\n\"/>').title()
            project_name = line.partition("name=\"")[2].rstrip('\n\"/>')
            
    return project_name
            
def backup_old_builds(build_directory):
    app_directory = "{}/{}.app".format(build_directory, get_project_name())
    if os.path.isdir(app_directory):
        os.rename(app_directory, "{}.{}".format(app_directory, datetime.datetime.now().timestamp()))
 
def create_directory_tree(build_directory):
    directories = ["Resources","MacOS"]
    for directory in directories:
        os.makedirs("{}{}.app/Contents/{}".format(build_directory, get_project_name(), directory))

def publish_app():
    publish_command = shlex.split("dotnet publish -c Release -r osx-x64 /p:PublishReadyToRun=false /p:TieredCompilation=false --self-contained")
    try:
        subprocess.run(publish_command,check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        logging.error(str(err.output))


def create_infoplist():       
    values = { "CFBundleExecutable":get_project_name(),
                "LSMinimumSystemVersion":platform.mac_ver()[0],
                "NSHumanReadableCopyright":"Copyright © {}".format(datetime.datetime.today().year)
    }       
    with open ('Info.plist', 'w') as f:
        f.write(Template(open("templates/Info.plist").read()).substitute(values))


def copy_sources():
    copytree("bin/Release/netcoreapp3.1/osx-x64/publish/Content", "bin/Release/osx-64/{}.app/Contents/Resources/Content".format(get_project_name()))
    copytree("bin/Release/netcoreapp3.1/osx-x64/publish/", "bin/Release/osx-64/{}.app/Contents/MacOS/".format(get_project_name()), dirs_exist_ok=True, ignore=ignore_patterns("Content"))

def main():    
    build_directory = "bin/Release/osx-64/"
    create_infoplist()
    backup_old_builds(build_directory)
    create_directory_tree(build_directory)
    publish_app()
    copy_sources()

if __name__ == "__main__":    
    main()