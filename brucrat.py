# coding: utf-8

'''
Tools to download Brucrat.js
'''

import os, tools

'''
URL for latest Brucrat.js Javascript file.
'''
DOWNLOAD_URL = 'https://raw.github.com/ademilsonfp/brucrat.js/master/js/brucrat.js'

def install(path):
  '''
  If not installed, download Brucrat.js.
  '''
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, tools.path(path))
    print 'brucrat installed'
