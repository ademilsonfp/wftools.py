# coding: utf-8

import os, tools, paths

DOWNLOAD_URL = 'http://underscorejs.org/underscore.js'
PATH_JS = 'underscore.js'

def install():
  path = paths.js(PATH_JS)
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, path)
    print 'underscore installed'
