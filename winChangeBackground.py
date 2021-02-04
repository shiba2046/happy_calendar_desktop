#!/usr/bin/env python3

import os, sys

# Function to actually set the wallpaper as tiled image
# > We will set background as a single image (which is 2 images merged)
def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "1")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)


if __name__ == '__main__':
  args = sys.argv
  if len(args) == 1:
    print(f'''
    To change the Windows background picture
    Can only be run in Windows enviroment.
    Usage: {args[0]} filename
    ''')
    exit()

  if os.name == 'nt':
    # Only import when in Windows
    
    import win32api, win32con, win32gui
    path = args[1]
    if os.path.exists(path):
      setWallpaper(args[1])
    else:
      raise RuntimeError(f'File {path} does not exist')
  else:
    raise RuntimeError('Cannot run in non-Windows Enviroment')