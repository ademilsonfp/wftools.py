# coding: utf-8

import os, tools, paths, underscore, jquery

DOWNLOAD_URL = 'http://backbonejs.org/backbone.js'
PATH_JS = 'backbone.js'

def install():
  jquery.install()
  underscore.install()

  path = paths.js(PATH_JS)
  if not os.path.exists(path):
    tools.download(DOWNLOAD_URL, path)
    print 'backbone installed'
