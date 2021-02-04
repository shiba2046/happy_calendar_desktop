#!/usr/bin/env python3
'''
wsl.py
A wrapper to provide a common interface for both Windows and WSL enviroment
Written by: Chiba2046
Last modifed: 04 Jan 2021

'''
import os
import subprocess
from pathlib import Path


# TODO: Wrap things in a class?
def wslToWinPath(path):
  # WSL path
  try:
    p = subprocess.run(['wsl', 'wslpath', '-w', path])
    return Path(p.stdout.decode().strip())
  except:
    pass

if os.name == 'nt':
  USERPROFILE = Path(os.getenv('USERPROFILE').strip())
  USERPROFILE_win = USERPROFILE
else:
  try:
    _user_profile = subprocess.run(['wslvar', 'USERPROFILE'], capture_output=True)
    _result = subprocess.run(['wslpath', _user_profile.stdout.decode()], capture_output=True)
    USERPROFILE = Path(_result.stdout.decode().strip())
    USERPROFILE_win = Path(_user_profile.stdout.decode().strip())

  except:
    pass
