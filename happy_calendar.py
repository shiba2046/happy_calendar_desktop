#!/usr/bin/env python3

""" 
Download happy calendar

"""
import requests
from bs4 import BeautifulSoup
# import re
import qrcode
from PIL import Image

import os
if os.name == "posix":
    folder = "/mnt/c"
else:
    folder = "C:"

# TODO:    
path = folder +'/Users/peng.f/Pictures/desktop-background/happiness_calender.jpg'

def getURL(href):
  return 'https://www.actionforhappiness.org' + href

def getCalendar():
  # Get the directorypage
  #r = requests.get(getURL('/calendars')) 
  r = requests.get(URL / 'calendars') 
  if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Find the first img tag with width=400
    # Get parents, and href
    month_url = soup.find('img', attrs={'width':'400'}).parent.attrs['href']
    print(f'Month URL: {month_url}')
    
    r = requests.get(getURL(month_url))
    if r.status_code == 200:
      soup = BeautifulSoup(r.text, 'html.parser')
      
      image_url = soup.find(lambda el: el.name == 'a' and 'JPG' in el.text).attrs['href']
      print(f'Image URL: {image_url}')
      r = requests.get(getURL(image_url), stream=True)
      if r.status_code == 200:
        #with open('calendar.jpg', 'wb') as f:
        with open(path, 'wb') as f:
          for chunk in r.iter_content(1024):
            f.write(chunk)



if __name__ == '__main__':
  getCalendar()
