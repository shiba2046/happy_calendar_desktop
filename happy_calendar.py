#!/usr/bin/env python3
""" 
happy_calendar.py
Download happy calendar
Written by: Chiba2046
Last modifed: 04 Jan 2021

"""
import requests
from bs4 import BeautifulSoup
from PIL import Image
import wsl
import os, sys
from pathlib import Path

calendar_jpg = wsl.USERPROFILE / 'Pictures/desktop-background/right/happiness_calender.jpg'

def getURL(href):
  return requests.compat.urljoin('https://www.actionforhappiness.org', href)

def getCalendar():
  # Get the directorypage
  r = requests.get(getURL('/calendars')) 
  
  if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Find the first img tag with width=400
    # Get parents, and href
    month_url = soup.find('img', attrs={'width':'400'}).parent.attrs['href']
    print(f'Month URL: {month_url}')
    
    r = requests.get(getURL(month_url))
    if r.status_code == 200:
      soup = BeautifulSoup(r.text, 'html.parser')
      
      # Find the URL to the actual calendar JPG
      image_url = soup.find(lambda el: el.name == 'a' and 'JPG' in el.text).attrs['href']
      print(f'Image URL: {image_url}')
      r = requests.get(getURL(image_url), stream=True)
      
      if r.status_code == 200:
        with open(calendar_jpg, 'wb') as f:
          for chunk in r.iter_content(1024):
            f.write(chunk)
        print(f'Written to {calendar_jpg}')


if __name__ == '__main__':
  getCalendar()
  import bgChanger3

  # from winChangeBackground import setWallpaper
  
  # if os.name == 'nt':
  #   # Only import when in Windows
    
  #   import win32api, win32con, win32gui
  #   path = Path(r'C:\Users\peng.f\Pictures\desktop-background\final.jpg')

  #   if path.is_file():
  #     setWallpaper(path)
    
  #     raise RuntimeError(f'File {path} does not exist')
  # else:
  #   raise RuntimeError('Cannot run in non-Windows Enviroment')
