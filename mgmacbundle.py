#!/usr/bin/env python3
import subprocess
import shlex

publish_command = shlex.split("dotnet publish -c Release -r osx-x64 /p:PublishReadyToRun=false /p:TieredCompilation=false --self-contained")

try:
    subprocess.run(publish_command,check=True, capture_output=True)
except subprocess.CalledProcessError as err:
    print(err.output)

