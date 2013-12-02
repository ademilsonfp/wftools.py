# coding: utf-8

'''
A serie of common tools used by other scripts.
'''

import os, sys, pickle, datetime, urllib2
from glob import glob
from itertools import chain
from cache import path as get_cache

'''
Buffer size for downloads.
'''
DOWNLOAD_BUFFER = 1024

def path(path, create_dirs=True):
  '''
  Create parent directories of a specified path when `create_dirs` flag is
  marked.
  '''
  create_basename = (os.path.sep == path[-1])
  path = dirs = os.path.realpath(path)
  if create_dirs:
    if not create_basename:
      dirs = os.path.dirname(path)
    if 0 < len(dirs) and not os.path.exists(dirs):
      os.makedirs(dirs)
  return path

def subpath(path):
  '''
  Returns the path relative to working directory.
  '''
  cwd = os.getcwd()
  if path.startswith(cwd):
    return path[len(cwd) + 1:]
  return path

def download(url, path):
  '''
  HTTP download with progress bar.
  '''
  print 'downloading %s...' % url

  urlopener = urllib2.build_opener()
  urlopener.addheaders = [('User-agent', 'wftools.py')]

  response = urlopener.open(url)
  size = int(response.headers.get('content-length', 0))
  buf_size = DOWNLOAD_BUFFER
  loaded = 0
  try:
    with open(path, 'w') as f:
      chunk = response.read(buf_size)
      while '' != chunk:
        f.write(chunk)

        # drawing bar
        if 0 < size:
          loaded += len(chunk)
          bar_size = 30
          per_size = bar_size * loaded / size
          res_size = bar_size * (size - loaded) / size
          per = str(100 * loaded / size)
          line_size = bar_size + 4 + len(per)

          bar_tpl = '%s[%s%s] %s%%'
          bar_fill = ('\r' * line_size, ':' * per_size, ' ' * res_size, per)
          sys.stdout.write(bar_tpl % bar_fill)

        chunk = response.read(buf_size)
  except KeyboardInterrupt as e:
    os.remove(path)

    # erase bar, print message and raise interruption
    msg = 'download removed %s' % path
    if 0 < size:
      msg += ' ' * max(0, line_size - len(msg))
      sys.stdout.write(('\r' * line_size))
    print msg
    raise e

  # erase bar and print message
  msg = 'download saved %s' % path
  if 0 < size:
    msg += ' ' * max(0, line_size - len(msg))
    sys.stdout.write(('\r' * line_size))
  print msg

def watch(src, fn, cache_name):
  '''
  Watch for file name patterns and executes a function when updates occur.

  The callback function must receive an argument which will be the list of
  updated files.
  '''
  cache = {}
  cache_path = get_cache(cache_name)
  if os.path.exists(cache_path):
    with open(cache_path, 'r') as stored:
      cache = pickle.load(stored)

  fpaths = chain(*[glob(patt) for patt in src])
  removed = cache.copy()
  updated = []
  for path in fpaths:
    removed.pop(path, None)
    lmtime = cache.get(path, None)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    if None is lmtime or lmtime < mtime:
      cache[path] = mtime
      updated.append(path)

  for path in removed:
    updated.append(path)
    del cache[path]

  if 0 < len(updated):
    fn(updated)
    with open(cache_path, 'w') as store:
      pickle.dump(cache, store)
