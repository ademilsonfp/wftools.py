# coding: utf-8

import os, shutil, paths, tools, jquery

from fnmatch import fnmatch
from zipfile import ZipFile

VERSION = '3.0.1'
DOWNLOAD_URL = 'https://github.com/twbs/bootstrap/archive/v%s.zip' % VERSION

PATH_JS = 'bootstrap.js'
PATH_LESS = 'bootstrap/%s'
PATH_FONT = '%s'

PKG_NAME = 'bootstrap.zip'
PKG_ROOT = 'bootstrap-%s' % VERSION
PKG_JS = '%s/dist/js/bootstrap.js' % PKG_ROOT
PKG_LESS = '%s/less/*' % PKG_ROOT
PKG_FONT = '%s/fonts/*' % PKG_ROOT

def download():
  pkg_path = paths.cache(PKG_NAME)
  if not os.path.exists(pkg_path):
    tools.download(DOWNLOAD_URL, pkg_path)
    print 'bootstrap downloaded'

def _install(js=True, font=True, less=True):
  if not js and not font and not less:
    return
  elif js:
    jquery.install()

  download()
  pkg_path = paths.cache(PKG_NAME)
  with ZipFile(pkg_path, 'r') as pkg:
    cache_path = paths.cache()
    new_path = paths.js(PATH_JS)
    if js and not os.path.exists(new_path):
      old_path = paths.cache(PKG_JS)
      pkg.extract(PKG_JS, cache_path)
      os.rename(old_path, new_path)
      print 'bootstrap js installed'

    if less or font:
      for entry in pkg.namelist():
        bname = os.path.basename(entry)
        old_path = paths.cache(entry)
        new_path = None
        entry_type = None
        if less and fnmatch(entry, PKG_LESS):
          new_path = paths.less(PATH_LESS % bname)
          entry_type = 'less'
        elif font and fnmatch(entry, PKG_FONT):
          new_path = paths.font(PATH_FONT % bname)
          entry_type = 'font'

        if None is not new_path and not os.path.exists(new_path):
          pkg.extract(entry, cache_path)
          os.rename(old_path, new_path)
          print 'bootstrap %s %s installed' % (entry_type, bname)

  shutil.rmtree(paths.cache(PKG_ROOT))

def install():
  _install()

def install_js():
  _install(font=False, less=False)

def install_font():
  _install(js=False, less=False)

def install_less():
  _install(False, False)
