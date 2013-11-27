# coding: utf-8

'''
A serie of common tools used by other scripts.
'''

import os, sys, pickle, datetime, urllib2, settings
from glob import glob

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
    if 1 > len(dirs) and not os.path.exists(dirs):
      os.path.makedirs(dirs)
  return path

def subpath(path):
  '''
  Returns the path relative to working directory.
  '''
  cwd = os.getcwd()
  l = len(cwd)
  if cwd == path[:l]:
    return path[l + 1:]
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
  bufsize = settings.DOWNLOAD_BUFFER
  loaded = 0
  try:
    with open(path, 'w') as f:
      chunk = response.read(bufsize)
      while '' != chunk:
        f.write(chunk)
        if 0 < size:
          loaded += len(chunk)
          bs = 30
          pl = bs * loaded / size
          pr = bs * (size - loaded) / size
          per = str(100 * loaded / size)
          ls = bs + 4 + len(per)
          pout = ('\r' * ls, ':' * pl, ' ' * pr, per)
          sys.stdout.write('%s[%s%s] %s%%' % pout)
        chunk = response.read(bufsize)
  except KeyboardInterrupt as e:
    os.remove(path)
    msg = 'download removed %s' % path
    if 0 < size:
      msg += ' ' * max(0, ls - len(msg))
      sys.stdout.write(('\r' * ls))
    print msg
    raise e

  msg = 'download saved %s' % path
  if 0 < size:
    msg += ' ' * max(0, ls - len(msg))
    sys.stdout.write(('\r' * ls))
  print msg

def watch(src, fn, cache_path):
  '''
  Watch for file name patterns and executes a function when updates occur.

  The callback function must receive an argument which will be the list of
  updated files.
  '''
  if not os.path.exists(cache_path):
    cache = {}
  else:
    with open(cache_path, 'r') as stored:
      cache = pickle.load(stored)

  fpaths = []
  for pattern in src:
    fpaths += glob(pattern)

  updated = []
  removed = fpaths[:]
  for path in fpaths:
    removed.remove(path)
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
