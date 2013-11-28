# coding: utf-8

import os, shutil, paths, tools, jquery, cache

from fnmatch import fnmatch
from zipfile import ZipFile

'''
Bootstrap version.
'''
VERSION = '3.0.2'

'''
Download URL.
'''
DOWNLOAD_URL = 'https://github.com/twbs/bootstrap/archive/v%s.zip' % VERSION

'''
Cache path to downloaded zip package.
'''
DOWNLOAD_CACHE = 'bootstrap.zip'

'''
Cache directory to extract files.
'''
UNZIP_CACHE = ''

'''
Root directory inside ZIP package.
'''
ZIP_ROOT = 'bootstrap-%s' % VERSION

'''
Path of JS file inside ZIP package.
'''
ZIP_JS_PATH = '%s/dist/js/bootstrap.js' % ZIP_ROOT

'''
Directory of CSS files inside ZIP package.
'''
ZIP_CSS_PATH = '%s/dist/css' % ZIP_ROOT

'''
Directory of CSS files inside ZIP package.
'''
ZIP_LESS_PATH = '%s/less' % ZIP_ROOT

'''
Directory of CSS files inside ZIP package.
'''
ZIP_FONT_PATH = '%s/dist/fonts' % ZIP_ROOT

def download():
  '''
  Download sources as zip package if is not cached.
  '''
  cache_path = cache.path(DOWNLOAD_CACHE)
  if not os.path.exists(cache_path):
    tools.download(DOWNLOAD_URL, cache_path)
    print 'bootstrap downloaded'
  return cache_path

def unzip_path(path='', create_dirs=True):
  '''
  Returns full path prepended with directory of unzipped files and creates
  parent directories when ``create_dirs`` flag is marked.
  '''
  return cache.path(os.path.join(UNZIP_CACHE, path), create_dirs)

def unzip(include=None, exclude=None):
  '''
  Download sources and extracts files to cache.

  You can specify files to be include or exclude using the respective
  parameters.

  Returns the list of unzipped files.
  '''
  extracted = []
  cache_path = unzip_path()
  zip_path = download()
  with ZipFile(zip_path, 'r') as pkg:
    if None is include and None is exclude:
      pkg.extractall(cache_path)
      return pkg.namelist()
    else:
      if None is include:
        include = ['*']
      elif isinstance(include, str):
        include = [include]

      for zip_file in pkg.namelist():
        if not zip_file.startswith(ZIP_CSS_PATH):
          continue

        name = os.path.basename(zip_file)
        add = False
        for patt in include:
          add = fnmatch(name, patt)
          if add:
            break

        if add and None is not exclude:
          if isinstance(exclude, str):
            add = add and not fnmatch(name, exclude)
          else:
            for patt in exclude:
              add = add and not fnmatch(name, exclude)
              if not add:
                break

        if add:
          pkg.extract(zip_file, cache_path)
          extracted.append(zip_file)
  return extracted

def install_js(path):
  '''
  Download sources and extracts Javascript file to specified path.
  '''
  if os.path.exists(path):
    return

  zip_path = download()
  cache_path = cache.path(UNZIP_CACHE)
  with ZipFile(zip_path, 'r') as pkg:
    pkg.extract(ZIP_JS_PATH, cache_path)
    os.rename(unzip_path(ZIP_JS_PATH), path)

def install_css(path, include=None, exclude=None):
  '''
  Download sources and extracts CSS files to specified path.

  You can specify names to be include or exclude using the respective
  parameters.

  Returns name list of installed files.
  '''
  if None is include:
    include = os.path.join(ZIP_CSS_PATH, '*')
  elif isinstance(include, str):
    include = os.path.join(ZIP_CSS_PATH, include)
  else:
    include = [os.path.join(ZIP_CSS_PATH, p) for p in include]

  if None is not exclude:
    if isinstance(exclude, str):
      exclude = os.path.join(ZIP_CSS_PATH, exclude)
    else:
      exclude = [os.path.join(ZIP_CSS_PATH, p) for p in exclude]

  extracted = unzip(include, exclude)
  installed = []
  for entry in extracted:
    name = os.path.basename(entry)
    os.rename(unzip_path(entry, False), os.path.join(path, name))
    installed.append(name)
  return installed

def install_less(path, include=None, exclude=None):
  '''
  Download sources and extracts LESS files to specified path.

  You can specify names to be include or exclude using the respective
  parameters.

  Returns name list of installed files.
  '''
  if None is include:
    include = os.path.join(ZIP_LESS_PATH, '*')
  elif isinstance(include, str):
    include = os.path.join(ZIP_LESS_PATH, include)
  else:
    include = [os.path.join(ZIP_LESS_PATH, p) for p in include]

  if None is not exclude:
    if isinstance(exclude, str):
      exclude = os.path.join(ZIP_LESS_PATH, exclude)
    else:
      exclude = [os.path.join(ZIP_LESS_PATH, p) for p in exclude]

  extracted = unzip(include, exclude)
  installed = []
  for entry in extracted:
    name = os.path.basename(entry)
    os.rename(unzip_path(entry, False), os.path.join(path, name))
    installed.append(name)
  return installed

def install_font(path, include=None, exclude=None):
  '''
  Download sources and extracts font files to specified path.

  You can specify names to be include or exclude using the respective
  parameters.

  Returns name list of installed files.
  '''
  if None is include:
    include = os.path.join(ZIP_FONT_PATH, '*')
  elif isinstance(include, str):
    include = os.path.join(ZIP_FONT_PATH, include)
  else:
    include = [os.path.join(ZIP_FONT_PATH, p) for p in include]

  if None is not exclude:
    if isinstance(exclude, str):
      exclude = os.path.join(ZIP_FONT_PATH, exclude)
    else:
      exclude = [os.path.join(ZIP_FONT_PATH, p) for p in exclude]

  extracted = unzip(include, exclude)
  installed = []
  for entry in extracted:
    name = os.path.basename(entry)
    os.rename(unzip_path(entry, False), os.path.join(path, name))
    installed.append(name)
  return installed
