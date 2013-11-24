# coding: utf-8

import os, tools, paths

JS_URL = 'http://code.jquery.com/qunit/qunit-1.12.0.js'
PATH_JS = 'test/qunit.js'

CSS_URL = 'http://code.jquery.com/qunit/qunit-1.12.0.css'
PATH_CSS = 'test/qunit.css'

def install():
  path = paths.js(PATH_JS)
  if not os.path.exists(path):
    tools.download(JS_URL, path)
    print 'qunit js installed'

  path = paths.css(PATH_CSS)
  if not os.path.exists(path):
    tools.download(CSS_URL, path)
    print 'qunit css installed'
