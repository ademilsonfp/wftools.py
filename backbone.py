# coding: utf-8

'''
Tools to install Backbone.js
'''

import os, tools

'''
Download URL for latest Backbone.js version.
'''
DOWNLOAD_URL = 'http://backbonejs.org/backbone.js'

def install(path):
  '''
  If not installed, download the latest version of Backbone.js to specified
  path.
  '''
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, tools.path(path))
    print 'backbone installed'
