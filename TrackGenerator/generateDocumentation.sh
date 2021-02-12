#!/bin/bash

snap install powershell --classic
sudo apt install python3 -y
pwsh GenerateDocumentation.ps1
