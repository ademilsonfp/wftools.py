# coding: utf-8

'''
Tools to install Font Awesome resources.
'''

import os, tools, cache

from fnmatch import fnmatch
from zipfile import ZipFile

'''
Font Awesome version.
'''
VERSION = '4.0.3'

'''
Download URL.
'''
DOWNLOAD_URL = 'http://fontawesome.io/assets/font-awesome-%s.zip' % VERSION

'''
Cache path to downloaded zip package.
'''
DOWNLOAD_CACHE = 'font-awesome.zip'

'''
Cache directory to extract files.
'''
UNZIP_CACHE = ''

'''
Root directory inside ZIP package.
'''
ZIP_ROOT = 'font-awesome-%s' % VERSION

'''
Directory of CSS files inside ZIP package.
'''
ZIP_CSS_PATH = '%s/css' % ZIP_ROOT

'''
Directory of LESS files inside ZIP package.
'''
ZIP_LESS_PATH = '%s/less' % ZIP_ROOT

'''
Directory of FONT files inside ZIP package.
'''
ZIP_FONT_PATH = '%s/fonts' % ZIP_ROOT

def download():
  '''
  Download sources as zip package if is not cached.
  '''
  cache_path = cache.path(DOWNLOAD_CACHE)
  if not os.path.exists(cache_path):
    tools.download(DOWNLOAD_URL, cache_path)
    print 'font awesome downloaded'
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
        add = False
        for patt in include:
          add = fnmatch(zip_file, patt)
          if add:
            break

        if add and None is not exclude:
          if isinstance(exclude, str):
            add = add and not fnmatch(zip_file, exclude)
          else:
            for patt in exclude:
              add = add and not fnmatch(zip_file, exclude)
              if not add:
                break

        if add:
          pkg.extract(zip_file, cache_path)
          extracted.append(zip_file)
  return extracted

def install_css(path, include=None, exclude=None):
  '''
  Download sources and extracts CSS files to specified path.

  You can specify names to be include or exclude using the respective
  parameters.

  Returns name list of installed files.
  '''
  if None is include:
    include = os.path.join(ZIP_CSS_PATH, '*.css')
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
    entry_path = unzip_path(entry, False)
    install_path = os.path.join(path, name)
    if not os.path.exists(install_path):
      tools.path(install_path)
      os.rename(entry_path, install_path)
      installed.append(name)
    else:
      os.unlink(entry_path)

  if 0 < len(installed):
    print 'installed font awesome css files'
  return installed

def install_less(path, include=None, exclude=None):
  '''
  Download sources and extracts LESS files to specified path.

  You can specify names to be include or exclude using the respective
  parameters.

  Returns name list of installed files.
  '''
  if None is include:
    include = os.path.join(ZIP_LESS_PATH, '*.less')
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
    entry_path = unzip_path(entry, False)
    install_path = tools.path(os.path.join(path, name))
    if not os.path.exists(install_path):
      tools.path(install_path)
      os.rename(entry_path, install_path)
      installed.append(name)
    else:
      os.unlink(entry_path)

  if 0 < len(installed):
    print 'installed font awesome less files'
  return installed

def install_font(path, include=None, exclude=None):
  '''
  Download sources and extracts font files to specified path.

  You can specify names to be include or exclude using the respective
  parameters.

  Returns name list of installed files.
  '''
  if None is include:
    include = os.path.join(ZIP_FONT_PATH, '*.*')
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
    entry_path = unzip_path(entry, False)
    install_path = tools.path(os.path.join(path, name))
    if not os.path.exists(install_path):
      tools.path(install_path)
      os.rename(entry_path, install_path)
      installed.append(name)
    else:
      os.unlink(entry_path)

  if 0 < len(installed):
    print 'installed font awesome font files'
  return installed
