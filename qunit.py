# coding: utf-8

'''
Tools to install QUnit.
'''

import os, tools

'''
QUnit version.
'''
VERSION = '1.12.0'

'''
Download URL of QUnit Javascript file.
'''
JS_DOWNLOAD_URL = 'http://code.jquery.com/qunit/qunit-%s.js' % VERSION

'''
Download URL of QUnit CSS file.
'''
CSS_DOWNLOAD_URL = 'http://code.jquery.com/qunit/qunit-%s.css' % VERSION

def install(js_path, css_path):
  '''
  If not installed, download Javascript and CSS file to specified paths.
  '''
  install_js(js_path)
  install_css(css_path)

def install_js(path):
  '''
  If not installed, download QUnit Javascript file to specified path.
  '''
  if not os.path.exists(path):
    tools.download(JS_DOWNLOAD_URL, tools.path(path))
    print 'qunit js installed'

def install_css(path):
  '''
  If not installed, download QUnit CSS file to specified path.
  '''
  if not os.path.exists(path):
    tools.download(CSS_DOWNLOAD_URL, tools.path(path))
    print 'qunit css installed'
