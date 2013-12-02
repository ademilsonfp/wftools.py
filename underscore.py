# coding: utf-8

'''
Tools to install Underscore.js
'''

import os, tools

'''
Download URL for latest Underscore.js version.
'''
DOWNLOAD_URL = 'http://underscorejs.org/underscore.js'

def install(path):
  '''
  If not installed, download latest version of underscore.js in specified path.
  '''
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, tools.path(path))
    print 'underscore installed'
