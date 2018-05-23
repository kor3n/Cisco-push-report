# Cisco-push-report
A Script to push commands to Cisco devices and get a report based on conditions.

# Prerequisites 
1. Python 3
2. install **parmiko** via pip use **--trusted-host** flag if needed.

# Usage
1. Configure the **pushsettings.conf** (See existing for example).
2. Configure the **options\settings.py** (With user and pass and if enable config is needed).
3. Run from cmd/powershell/terminal via: push.py
* Current bug in above - See to do


1. Configure the **report\checks.py** (See existing for example).
2. Configure the **options\settings.py** (With user and pass and if enable config is needed).
Run from cmd/powershell/terminal via: report.py -i <IP ADDRESS>
* Current bug in above only -i flag works - See to do 

# To do
1. Sort out command line arguments not changing settings - currently have to change settings.py.
