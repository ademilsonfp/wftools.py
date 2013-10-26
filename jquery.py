# coding: utf-8

import os, tools, paths

DOWNLOAD_URL = 'http://code.jquery.com/jquery-1.10.2.js'
PATH_JS = 'jquery.js'

def install():
  path = paths.js(PATH_JS)
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, path)
  print 'jquery installed'
