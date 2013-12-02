# coding: utf-8

'''
Tools to install jQuery.
'''

import os, tools

'''
jQuery version.
'''
VERSION = '1.10.2'

'''
Download URL.
'''
DOWNLOAD_URL = 'http://code.jquery.com/jquery-%s.js' % VERSION

def install(path):
  '''
  If not installed, download the jQuery file to specified path.
  '''
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, tools.path(path))
    print 'jquery installed'
