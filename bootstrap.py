# coding: utf-8

import os, shutil, paths, tools

from fnmatch import fnmatch
from zipfile import ZipFile
from glob import glob

VERSION = '3.0.0'
DOWNLOAD_URL = 'https://github.com/twbs/bootstrap/archive/v%s.zip' % VERSION

PKG_JS = 'bootstrap-%s/dist/js/bootstrap.js' % VERSION
PKG_LESS = 'bootstrap-%s/less/*' % VERSION
PKG_FONT = 'bootstrap-%s/fonts/*' % VERSION

PATHP_JS = '%s'
PATHP_LESS = 'bootstrap/%s'
PATHP_FONT = '%s'
PATHP_CACHE = '%s'

def install():
  pkg_path = paths.cache('bootstrap.zip')
  if not os.path.exists(pkg_path):
    tools.download(DOWNLOAD_URL, pkg_path)

  with ZipFile(pkg_path, 'r') as pkg:
    cache_path = paths.cache(PATHP_CACHE % '')
    pkg.extract(PKG_JS, cache_path)
    for entry in pkg.namelist():
      if fnmatch(entry, PKG_LESS) or fnmatch(entry, PKG_FONT):
        pkg.extract(entry, cache_path)

  ext_js, ext_less, ext_font = (paths.cache(PATHP_CACHE % p) \
      for p in (PKG_JS, PKG_LESS, PKG_FONT))

  fname = os.path.basename(ext_js)
  os.rename(ext_js, paths.js(PATHP_JS % fname))

  for entry in glob(ext_less):
    fname = os.path.basename(entry)
    os.rename(entry, paths.less(PATHP_LESS % fname))

  for entry in glob(ext_font):
    fname = os.path.basename(entry)
    os.rename(entry, paths.font(PATHP_FONT % fname))

  shutil.rmtree(paths.cache('bootstrap-%s' % VERSION))
  print 'bootstrap installed'
